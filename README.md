# General Fitness Block A

12 weeks. Starts Tuesday 15 September 2026.

Built after the Colorado 100. Priorities, in order: upper body definition, midsection fat loss,
cardiovascular conditioning, lower body maintenance.

---

## The week

| Day | Session | Time |
|---|---|---|
| Monday | Off | — |
| Tuesday | Upper A, push | 75 min |
| Wednesday | Zone 2 cardio | 50 min |
| Thursday | VO2max intervals | 40 min |
| Friday | Upper B, pull | 75 min |
| Saturday | Lower body, machines | 85 min |
| Sunday | Easy cardio, optional | 45-75 min |

Sunday is the drop day. Skipping it in a bad week costs you nothing. Skipping Thursday does.

### Why it is shaped this way

Two upper days against one lower day is deliberate. Your hike block ran the opposite ratio for
22 weeks, which is exactly why your legs look trained and your upper body does not. Legs are now
on maintenance. One quality session a week holds what you built.

Intervals sit on Thursday, two days clear of Saturday's leg work, so the two never compete.

---

## Heart rate

Max 180.

| Zone | BPM | Used for |
|---|---|---|
| Easy | under 122 | Sunday |
| Zone 2 | 122-144 | Wednesday, cooldowns |
| VO2max | 162-171 | Thursday intervals |

**Thursday, in full:** 10 min easy. Then 4 rounds of 4 minutes at 162-171 with 3 minutes easy
between. 5 min cooldown. Bike or rower, not running.

Weeks 1 and 2 do 3 rounds instead of 4. It takes roughly 90 seconds of each round to reach the
target heart rate, so start hard rather than building into it.

---

## Phases

| Weeks | Phase | What changes |
|---|---|---|
| 1-2 | Ramp-in | One less set per exercise. Stop 3-4 reps short. Find your loads. No hip thrust. |
| 3-6 | Build A | Full sets. Double progression starts. Hip thrust enters. |
| 7 | Deload | Two sets, 60% load, same reps. Mandatory. |
| 8-11 | Build B | Full sets, harder. Last set of the final exercise near failure. |
| 12 | Test | Light. Re-measure everything. |

**Double progression:** when you hit the top of the rep range on every working set, add weight next
session. 5 lbs upper body, 10 lbs lower body. That is the entire progression rule. Do not overthink it.

---

## Two standing rules

**Everything presses and rows seated or chest-supported in weeks 1 and 2.** Nothing loads the spine
while your back settles. Bent-over rowing does not appear in this program at all.

**Knee protection never comes out.** Lateral band walks in the warm-up, hip abduction machine, and
both calf raise variations. Even on a short day. That circuit is about ten minutes and it is the
reason the knee held up across 100 miles.

---

## Nutrition

| | Target |
|---|---|
| Calories | 2,450 |
| Protein | 180g |
| Carbs | 250g |
| Fat | 80g |
| Creatine | 5g daily, any time, no loading |

Protein is 180, not 215. A number you hit 90% of the time beats one you hit half the time, and the
research says everything above roughly 0.8g per pound is spare change.

**Four anchors and a nightcap. Stop thinking about protein the rest of the day.**

| When | What | Protein |
|---|---|---|
| Breakfast | Fairlife Core Power Elite, or whey plus liquid egg whites | 40g |
| Mid-morning | Greek yogurt or cottage cheese | 25g |
| Lunch | Rotisserie chicken or canned tuna | 45g |
| Dinner | Salmon, ground turkey, or shrimp | 45g |
| Before bed | Casein | 25g |

Shred the rotisserie chicken into portions on Sunday. Lunch is the meal that always falls short,
because it gets decided at 12:30 when you are busy.

If bodyweight has not moved after two full weeks of actually hitting these, drop 150 calories.

---

## What gets measured

**Weekly:** bodyweight and waist at the navel, both in the morning before food.

**Continuous:** resting heart rate, sleep and HRV from the ring. Session duration and average heart
rate from Garmin through Strava. Every working set in Hevy.

**Twelve week targets:** waist down 2 to 3 inches. Resting heart rate low to mid 50s, from 60.
Bodyweight somewhere around 188 to 191, carrying more upper body muscle than you do at 197.

Bodyweight is a data point, not the goal. If you gain upper body muscle while losing fat, the scale
will lie to you. The waist will not.

---

## Off the gym floor

Three things that are not workouts and matter anyway.

- **Take two or three phone meetings a day walking.** Ninety percent of your day is meetings and most
  of them are audio. Nine hours of sitting is an independent cardiovascular risk and morning
  training does not cancel it. This is worth more than a sixth gym day.
- **Standing desk from 20% to 40%.**
- **Ask about ApoB** on the next lipid panel, and about whether a calcium score fits your history.

---

## Starting weights

Pulled from your Phase 3 and Phase 4 logs, then discounted for the taper plus two weeks off.
These are starting points for weeks 1 and 2, not targets. Adjust on the floor and log what you
actually did.

| Exercise | Start |
|---|---|
| Incline dumbbell press | 30 lb dumbbells |
| Machine chest press | find it |
| Seated dumbbell shoulder press | 25 lb dumbbells |
| Dumbbell lateral raise | 12 lb dumbbells |
| Triceps pushdown | 40 lbs |
| Chest-supported row | 90 lbs |
| Lat pulldown | 100 lbs |
| Seated cable row | 90 lbs |
| Face pull | 30 lbs |
| Dumbbell curl | 20 lb dumbbells |
| Leg press | 160 lbs |
| Hip thrust machine (week 3+) | 90 lbs |
| Leg extension | 70 lbs |
| Seated leg curl | 70 lbs |
| Hip abduction | 70 lbs |
| Standing calf raise | 90 lbs |
| Seated calf raise | 45 lbs |

Your last logged numbers, for reference: dumbbell bench 45s for 10, dumbbell row 55s for 12,
barbell hip thrust 110, goblet squat 50, Bulgarian split squat 40s, leg press 200.

The pull numbers are estimates. You have never logged a pulldown or a cable row, so treat week 1
as finding them.

---

## Getting it into Hevy

```
export HEVY_API_KEY=your-key-here
cd ~/Documents/Claude/projects/WorkoutPlan
python3 push_to_hevy.py --dry-run
python3 push_to_hevy.py
```

The dry run matches every exercise against your Hevy library and prints what it found without
creating anything. Read that output first. If something says MISSING, say so and the movement gets
swapped for one Hevy knows.

Run it from Terminal on the Mac itself. It will not work from a sandboxed shell.

---

## Files

| File | What it is |
|---|---|
| `program.json` | The program as structured data. Source of truth. |
| `push_to_hevy.py` | Creates the routines in Hevy from program.json. |
| `export.html` | Drop into the CO100 repo to pull old logged weights off your phone. |
| `README.md` | This. |
