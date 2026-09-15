# GordoGains

16-week general fitness block. Week 1 starts Tuesday 15 September 2026.

Live page: https://gwcarlisle.github.io/GordoGains/

## What this is

Read-only training reference. Strength gets logged in **Hevy**. Every session gets recorded by
Garmin into **Strava**. This page just tells you what the day holds.

## Files

| File | What it is |
|---|---|
| `program.json` | The program. Source of truth. Edit this. |
| `build.py` | Reads program.json, writes index.html. |
| `index.html` | **Generated. Do not hand-edit, it gets overwritten.** |

## Rebuilding

```
python3 build.py
git add -A && git commit -m "rebuild" && git push
```

Standard library only. No dependencies.

The build refuses to write anything if it finds text that looks like a credential, in either the
data or the generated page. No API key belongs in this repo.

## The block

| Weeks | Dates | Phase |
|---|---|---|
| 1-2 | Sep 15 - Sep 28 | Re-entry |
| 3-6 | Sep 29 - Oct 26 | Accumulation 1 |
| 7 | Oct 27 - Nov 2 | Deload |
| 8-11 | Nov 3 - Nov 30 | Accumulation 2 |
| 12 | Dec 1 - Dec 7 | Deload |
| 13-14 | Dec 8 - Dec 21 | Intensification |
| 15 | Dec 22 - Dec 28 | Deload, placed on Christmas on purpose |
| 16 | Dec 29 - Jan 4 | Test and benchmark |

Monday is always off. Sunday is optional and is the day you drop in a bad week.

## The week

| Day | Session |
|---|---|
| Tue | Upper A, push |
| Wed | Zone 2 cardio |
| Thu | VO2max intervals |
| Fri | Upper B, pull |
| Sat | Lower, machines |
| Sun | Easy cardio, optional |

## Why it is built this way

**Two upper days against one lower day.** The hike block ran the opposite ratio for 22 weeks,
which is why the legs look trained and the upper body does not. Legs are now on maintenance.
The 2025 dose-response meta-regression found training frequency has a negligible effect on
hypertrophy once weekly volume is equal, so once a week for legs is fine.

**4x4 intervals at 90-95% of max HR.** Helgerud 2007 compared four protocols over 8 weeks.
Long slow distance and threshold work produced no significant VO2max change. The 4x4 produced
+7.2%, the best of the four. Target of 162-171 bpm is 90-95% of a 180 max.

**One interval session a week, not three.** The study used three. Three would compete with the
lifting and the sleep. A smaller gain sustained for 16 weeks beats the study protocol abandoned
in week five.

**Progression on intervals comes from rounds, round length and recovery. Never from a higher
heart rate.** 171 is already 95% of max. There is nowhere above it worth going.

**Knee protection never comes out.** Lateral band walks, hip abduction, both calf raise
variations. Every leg day, every week.
