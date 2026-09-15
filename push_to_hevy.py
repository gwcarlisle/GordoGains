#!/usr/bin/env python3
"""
Push the routines in program.json into Hevy.

Usage:
    export HEVY_API_KEY=your-key-here
    python3 push_to_hevy.py --dry-run     # match exercises, create nothing
    python3 push_to_hevy.py               # actually create the folder and routines

Standard library only. No pip install needed.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = "https://api.hevyapp.com/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM = os.path.join(HERE, "program.json")


def api(path, key, method="GET", body=None):
    url = path if path.startswith("http") else BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("api-key", key)
    req.add_header("accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        raise SystemExit("\nHevy API error %s on %s %s\n%s\n" % (e.code, method, url, detail))
    except urllib.error.URLError as e:
        raise SystemExit("\nCould not reach Hevy: %s\nCheck your network.\n" % e.reason)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def tokens(s):
    stop = {"the", "a", "machine", "cable", "dumbbell", "barbell", "seated", "standing"}
    return set(t for t in norm(s).split() if t and t not in stop)


def load_templates(key):
    out, page = {}, 1
    while True:
        res = api("/exercise_templates?page=%d&pageSize=100" % page, key)
        batch = res.get("exercise_templates") or []
        if not batch:
            break
        for t in batch:
            out[t["id"]] = t.get("title", "")
        if len(batch) < 100:
            break
        page += 1
        if page > 60:
            break
    return out


def match(name, templates):
    """Return (template_id, matched_title, confidence) or (None, None, 0)."""
    target_n = norm(name).split()
    target_set = tokens(name)
    best = (None, None, 0.0)
    for tid, title in templates.items():
        if norm(title) == norm(name):
            return (tid, title, 1.0)
        ts = tokens(title)
        if not ts or not target_set:
            continue
        overlap = len(target_set & ts) / len(target_set | ts)
        # small bonus when every word of the short program name appears in the title
        if all(w in norm(title).split() for w in target_n if w not in {"machine", "cable", "dumbbell"}):
            overlap += 0.25
        if overlap > best[2]:
            best = (tid, title, overlap)
    return best if best[2] >= 0.5 else (None, None, best[2])


def build_sets(ex):
    reps = str(ex.get("reps", ""))
    n = int(ex.get("sets", 3))
    if "sec" in reps.lower():
        secs = int(re.findall(r"\d+", reps)[0])
        return [{"type": "normal", "duration_seconds": secs} for _ in range(n)]
    nums = re.findall(r"\d+", reps)
    target = int(nums[0]) if nums else 10
    lbs = ex.get("start_lbs")
    # Do NOT round. Hevy stores kg and converts back for display, so a rounded
    # kg makes 160 lbs show as 160.06. Full precision round-trips exactly.
    kg = lbs * 0.45359237 if lbs else None
    return [{"type": "normal", "weight_kg": kg, "reps": target} for _ in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="match exercises but create nothing")
    ap.add_argument("--folder", default="General Fitness Block A")
    args = ap.parse_args()

    key = os.environ.get("HEVY_API_KEY", "").strip()
    if not key:
        raise SystemExit("Set HEVY_API_KEY first:\n  export HEVY_API_KEY=your-key-here")

    with open(PROGRAM) as f:
        program = json.load(f)

    print("Loading your Hevy exercise library...")
    templates = load_templates(key)
    print("  %d exercise templates found.\n" % len(templates))

    planned, problems = [], []
    for rk, routine in program["routines"].items():
        exercises = []
        print("%s" % routine["title"])
        for ex in routine["exercises"]:
            tid, title, conf = match(ex["name"], templates)
            if not tid:
                problems.append((routine["title"], ex["name"]))
                print("   MISSING  %-36s  (no match, best score %.2f)" % (ex["name"], conf))
                continue
            flag = "ok      " if conf >= 0.95 else "approx  "
            print("   %s %-36s -> %s" % (flag, ex["name"], title))
            note = ex.get("note", "")
            if ex.get("reps"):
                note = ("Target %s reps. " % ex["reps"]) + note
            if ex.get("start_lbs"):
                note = ("Start %s lbs. " % ex["start_lbs"]) + note
            exercises.append({
                "exercise_template_id": tid,
                "superset_id": None,
                "rest_seconds": int(ex.get("rest", 90)),
                "notes": note.strip()[:490],
                "sets": build_sets(ex),
            })
        planned.append({
            "title": routine["title"],
            "notes": routine.get("notes", "")[:490],
            "exercises": exercises,
        })
        print()

    if problems:
        print("Could not match %d exercise(s):" % len(problems))
        for r, n in problems:
            print("   %s / %s" % (r, n))
        print("Create these by hand in Hevy, or tell Claude and it will pick different movements.\n")

    if args.dry_run:
        print("Dry run. Nothing was created.")
        return

    print("Creating folder '%s'..." % args.folder)
    folder_id = None
    try:
        res = api("/routine_folders", key, "POST", {"routine_folder": {"title": args.folder}})
        folder_id = (res.get("routine_folder") or {}).get("id")
        print("  folder id %s\n" % folder_id)
    except SystemExit as e:
        print("  could not create folder (%s). Routines will go to the root.\n" % e)

    for r in planned:
        payload = {"routine": {
            "title": r["title"],
            "folder_id": folder_id,
            "notes": r["notes"],
            "exercises": r["exercises"],
        }}
        api("/routines", key, "POST", payload)
        print("  created: %s (%d exercises)" % (r["title"], len(r["exercises"])))

    print("\nDone. Open Hevy and pull to refresh.")


if __name__ == "__main__":
    main()
