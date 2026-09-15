#!/usr/bin/env python3
"""
Pull training data into stats.json. Run before build.py.

    export HEVY_API_KEY=...
    export STRAVA_REFRESH_TOKEN=...  STRAVA_CLIENT_ID=...  STRAVA_CLIENT_SECRET=...
    export ULTRAHUMAN_TOKEN=...      ULTRAHUMAN_EMAIL=...     # optional
    python3 fetch.py

Reads credentials from the environment ONLY. Never writes them to disk.
Writes only derived numbers into stats.json's "pulled" section; manual entries
in "weekly" are never touched.

Fails loudly. A source that errors leaves its previous data in place and the
run exits non-zero, so a half-empty page never gets published.
"""
import json, os, sys, datetime, urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = os.path.join(HERE, "stats.json")
PROGRAM = os.path.join(HERE, "program.json")
LB = 0.45359237

def get(url, headers=None, data=None, method="GET"):
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read().decode()
    return json.loads(raw) if raw.strip() else {}

def week_of(start, iso):
    d = datetime.date.fromisoformat(iso[:10])
    return (d - start).days // 7 + 1

# ---------- Hevy ----------
def hevy(start, weeks):
    key = os.environ.get("HEVY_API_KEY", "").strip()
    if not key:
        raise SystemExit("HEVY_API_KEY not set")
    h = {"api-key": key, "accept": "application/json"}
    out, page = [], 1
    while page <= 20:
        d = get(f"https://api.hevyapp.com/v1/workouts?page={page}&pageSize=10", h)
        batch = d.get("workouts") or []
        if not batch:
            break
        out += batch
        if len(batch) < 10:
            break
        page += 1

    sessions, strength = [], {}
    for w in out:
        st = w.get("start_time", "")
        if not st:
            continue
        wk = week_of(start, st)
        if wk < 1 or wk > weeks:
            continue
        sessions.append({"week": wk, "date": st[:10], "title": w.get("title", ""),
                         "exercises": len(w.get("exercises") or [])})
        for ex in w.get("exercises") or []:
            name = ex.get("title", "")
            best = 0.0
            for s in ex.get("sets") or []:
                kg = s.get("weight_kg")
                if kg:
                    best = max(best, kg / LB)
            if best:
                strength.setdefault(name, {})
                prev = strength[name].get(str(wk), 0)
                strength[name][str(wk)] = round(max(prev, best), 1)
    return sessions, strength

# ---------- Strava ----------
def strava(start, weeks):
    rt = os.environ.get("STRAVA_REFRESH_TOKEN", "").strip()
    cid = os.environ.get("STRAVA_CLIENT_ID", "").strip()
    cs = os.environ.get("STRAVA_CLIENT_SECRET", "").strip()
    if not (rt and cid and cs):
        print("  strava: credentials not set, skipping", file=sys.stderr)
        return None, None
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": cs,
                                   "grant_type": "refresh_token", "refresh_token": rt}).encode()
    tok = get("https://www.strava.com/oauth/token", {"Content-Type": "application/x-www-form-urlencoded"},
              data=body, method="POST")
    access, new_refresh = tok.get("access_token"), tok.get("refresh_token")
    h = {"Authorization": "Bearer " + access}
    after = int(datetime.datetime.combine(start, datetime.time()).timestamp())
    acts, page = [], 1
    while page <= 10:
        d = get(f"https://www.strava.com/api/v3/athlete/activities?after={after}&per_page=100&page={page}", h)
        if not d:
            break
        acts += d
        if len(d) < 100:
            break
        page += 1
    cardio = []
    for a in acts:
        wk = week_of(start, a.get("start_date_local", ""))
        if wk < 1 or wk > weeks:
            continue
        cardio.append({"week": wk, "date": a["start_date_local"][:10], "type": a.get("sport_type", ""),
                       "min": round((a.get("moving_time") or 0) / 60), "avg_hr": a.get("average_heartrate"),
                       "max_hr": a.get("max_heartrate")})
    return cardio, new_refresh

def main():
    program = json.load(open(PROGRAM))
    stats = json.load(open(STATS))
    start = datetime.date.fromisoformat(program["meta"]["start_date"])
    weeks = program["meta"]["weeks"]

    print("fetching Hevy...")
    sessions, strength = hevy(start, weeks)
    print(f"  {len(sessions)} sessions, {len(strength)} exercises with load")

    print("fetching Strava...")
    cardio, new_rt = strava(start, weeks)
    if cardio is not None:
        print(f"  {len(cardio)} activities")

    p = stats["pulled"]
    p["fetched_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    p["sessions"] = sessions
    p["strength"] = strength
    if cardio is not None:
        p["cardio"] = cardio

    blob = json.dumps(stats, indent=2)
    for env in ("HEVY_API_KEY", "STRAVA_CLIENT_SECRET", "STRAVA_REFRESH_TOKEN", "ULTRAHUMAN_TOKEN"):
        v = os.environ.get(env, "")
        if v and v in blob:
            raise SystemExit(f"ABORT: {env} leaked into stats.json. Nothing written.")
    with open(STATS, "w") as f:
        f.write(blob + "\n")
    print("wrote stats.json")
    if new_rt:
        print("\nNOTE: Strava issued a new refresh token. Update STRAVA_REFRESH_TOKEN.")
        print("      (In GitHub Actions the workflow writes this back to the secret automatically.)")

if __name__ == "__main__":
    main()
