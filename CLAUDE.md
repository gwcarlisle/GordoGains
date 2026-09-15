# GordoGains

Gordon's 16-week training block. Static site, no backend, no framework.
Live at https://gwcarlisle.github.io/GordoGains/ (path is case-sensitive).

## Rules

**Never hand-edit `index.html`.** It is generated. `python3 build.py` overwrites it.
Change `build.py` or `program.json` instead.

**No credential ever enters this repo.** Not in a file, not in a commit, not in the
generated page. `fetch.py` reads keys from the environment only. Both scripts abort
if key-shaped text reaches their output. Git history is permanent, so a leaked key
means rotating the key, not deleting a line.

**Keep `.nojekyll`.** Without it GitHub Pages runs Jekyll and serves README.md as the
homepage instead of index.html. This has already happened once.

## Files

| File | |
|---|---|
| `program.json` | The 16-week block. Source of truth for the plan. |
| `stats.json` | Weight, waist, resting HR, and data pulled from APIs. |
| `fetch.py` | Pulls Hevy and Strava into stats.json. Needs env vars. |
| `build.py` | program.json + stats.json -> index.html. Credential-free. |
| `index.html` | Generated. Do not touch. |

```
python3 fetch.py     # optional, needs keys in env
python3 build.py
git add -A && git commit -m "..." && git push
```

Standard library only. No dependencies, deliberately.

## Design decisions worth not undoing

**The strength chart is indexed to each lift's first logged week, not absolute pounds.**
Leg press at 160 and dumbbell bench at 30 on a shared pound axis makes the upper body
lines unreadable. Absolute weight lives in the tooltip.

**Weight and waist get separate charts.** Different scales. Never a dual axis.

**Series colors are validated**, not chosen by eye: `#3987e5 #d95926 #199e70 #c98500
#d55181` against the `#0c0e14` surface. They clear the colorblind separation threshold
and 3:1 contrast. Changing them means re-validating.

**Weight values sent to the Hevy API must be full precision** (`lbs * 0.45359237`,
not rounded). Hevy stores kilograms and converts back for display, so a rounded
kilogram makes 160 lbs render as 160.06.

**Hevy routines are addressed by ID, never by title.** Gordon renames them.
Read the routine, modify it, write it back, so his own edits survive.

## Where the reasoning lives

The training logic, the research behind it, and Gordon's constraints are in the
Health Journey project in Claude's Cowork app, not in this repo. Program changes
should be discussed there. This repo is the implementation.
