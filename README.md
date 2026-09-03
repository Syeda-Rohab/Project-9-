# Project 9: Rehearse a Routine for Free

Proves the A5 lesson without needing a paid Claude Pro/Max/Team plan
(which the real Claude Code Routines feature requires). Uses GitHub
Actions' manual "Run workflow" button as a free stand-in for a
one-off Routine run.

- **Time:** 20–30 min
- **Difficulty:** easy
- **Concepts used:** A1, A3 (one-off runs), A5 (reading runs, not status)

## Why not the real Routines feature?
Claude Code Routines (`/schedule`, `claude.ai/code/routines`) require
a Pro, Max, Team, or Enterprise plan. If you get one later, the real
version of this project is: create a routine whose prompt summarizes
yesterday's commits onto a `claude/summary` branch, fire it once with
`/schedule tomorrow at 9am, ...` or **Run now**, read the full
transcript. Then break the prompt (point it at a nonexistent file),
fire it again, and compare. Everything below teaches the identical
lesson for free.

## Files
| File | Role |
|---|---|
| `routine_task.py` | The "prompt" — summarizes commits, or (in fail mode) tries to read a file that doesn't exist |
| `.github/workflows/routine-rehearsal.yml` | Manual-trigger-only workflow — the free stand-in for a one-off run |

## The key design choice (this is the whole lesson)
In `routine_task.py`, the fail-mode path **catches** the missing-file
error and prints `TASK FAILED: ...` — it does **not** call
`sys.exit(1)`. This mirrors exactly how a real Claude Code Routine
behaves: the agent doesn't crash the session when a task-level thing
goes wrong, it just reports the problem conversationally and the
session still ends normally. That's why both runs come back green.

## Setup on GitHub (free, ~10 min)
1. Push this folder to a new GitHub repo (same steps as Project 6 —
   create a repo, upload these 3 files, keeping the
   `.github/workflows/routine-rehearsal.yml` path exactly as-is,
   lowercase).
2. Go to the **Actions** tab. You should see "Routine Rehearsal"
   listed on the left.
3. Click into it. You'll see a **"Run workflow"** button — this is
   your one-off run trigger, the free equivalent of `/schedule` or
   **Run now**.

## Run 1: the success case
1. Click **Run workflow**. In the dropdown, choose `mode: success`.
   Click the green **Run workflow** button to confirm.
2. Wait ~15 seconds, refresh. The run shows a **green checkmark** in
   the list.
3. **Click into the run itself** (not just the checkmark in the
   list) → click the `run-routine` job → expand **"Run the routine's
   task"**. Read the actual transcript:
   ```
   TASK SUCCEEDED: summary written to claude/summary branch.
   ```
4. Check the repo's branches — a new `claude/summary` branch now
   exists with a `SUMMARY.md` listing real commits.

## Run 2: the failure case
1. Click **Run workflow** again. This time choose `mode: fail`.
2. Wait, refresh. **This run also shows a green checkmark** — same
   as Run 1, indistinguishable from the status column alone.
3. Click into this run → expand **"Run the routine's task"** → read
   the transcript:
   ```
   TASK FAILED: could not find 'notes_that_do_not_exist.md'.
   No summary was written. A human should check why this file was
   expected to exist.
   ```
4. Confirm no new commit was pushed to `claude/summary` this time —
   the task genuinely did nothing useful, despite the green check.

## Done-when checklist
- [x] Two green runs exist in the Actions history.
- [x] Run 1's transcript shows real success (commits summarized,
      branch updated).
- [x] Run 2's transcript shows real failure (file not found, nothing
      written) — while still showing green in the list.

## The A5 lesson, in one sentence
**Green means the session ended without an infrastructure error —
nothing more; it says nothing about whether the task itself actually
succeeded, which you can only know by reading the transcript.**

## Why this matters for real Routines later
If you upgrade to a paid plan and use real Claude Code Routines, this
is exactly why the docs (and this project) insist you use **Run now**
and read the full transcript before ever putting a prompt on a
repeating schedule — a broken prompt on a daily cron would show up as
seven green checkmarks in a row, with seven silent no-ops behind them,
and nothing in the status column would ever tell you.
