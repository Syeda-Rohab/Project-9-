#!/usr/bin/env python
"""
routine_task.py — simulates a Claude Code Routine's prompt.

This mirrors how a real Routine behaves: if something inside the task
goes wrong (like a missing file), the agent doesn't crash the whole
session — it just reports the problem in its own transcript and the
session still ends normally. That's WHY the run shows green either
way: green means "the session ended without an infrastructure error,"
not "the task succeeded."

Usage:
    python routine_task.py success   -> summarizes real commits, writes
                                         them to claude/summary branch
    python routine_task.py fail      -> tries to read a file that does
                                         not exist, reports the failure
                                         in its own output, but the
                                         script itself still exits 0 —
                                         exactly like a real Routine's
                                         session completing normally
                                         even though the task failed.
"""

import subprocess
import sys
from datetime import datetime


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def do_success_task():
    print("--- Task: summarize recent commits onto claude/summary ---")
    log = run('git log -5 --pretty=format:"- %s"').stdout
    summary = f"# Commit Summary — {datetime.now():%Y-%m-%d}\n\n{log}\n"

    run("git checkout -b claude/summary")
    with open("SUMMARY.md", "w") as f:
        f.write(summary)
    run("git add SUMMARY.md")
    run('git commit -q -m "Add commit summary"')

    print(summary)
    print("TASK SUCCEEDED: summary written to claude/summary branch.")


def do_fail_task():
    print("--- Task: read notes from a file that does not exist ---")
    filename = "notes_that_do_not_exist.md"
    try:
        with open(filename) as f:
            f.read()
        print("TASK SUCCEEDED: read the file.")
    except FileNotFoundError:
        # This is the key behavior: the agent (or, here, our script)
        # catches the problem and reports it plainly instead of
        # crashing the whole run. The SESSION still ends normally.
        print(f"TASK FAILED: could not find '{filename}'. "
              f"No summary was written. A human should check why this "
              f"file was expected to exist.")
        # Deliberately NOT calling sys.exit(1) here — the session
        # itself completed fine; only the task inside it failed.
        # This is exactly what makes the run show green regardless.


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "success"
    print(f"=== Routine run starting, mode={mode} ===\n")
    if mode == "fail":
        do_fail_task()
    else:
        do_success_task()
    print("\n=== Session ended normally. (This is what makes it 'green'.) ===")
