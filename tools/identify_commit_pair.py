"""Identify the commit pair for the coverage protection policy: main_head and branch_head.

main_head is the latest commit on main, read from the remote. branch_head is the pull request's head on a
pull_request event, the dispatched commit on a workflow_dispatch, and HEAD when run locally.

Usage, from the repository root:  python tools/identify_commit_pair.py
Prints main_head=<sha> and branch_head=<sha>, and appends the same lines to $GITHUB_OUTPUT when it is set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    main_head, branch_head = identify_commit_pair()
    outputs = f"main_head={main_head}\nbranch_head={branch_head}\n"
    print(outputs, end="")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output_file:
            output_file.write(outputs)
    return 0


def identify_commit_pair() -> tuple[str, str]:
    main_head = git("ls-remote", "origin", "refs/heads/main").split()[0]
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        branch_head = event["pull_request"]["head"]["sha"]
    elif event_name == "workflow_dispatch":
        branch_head = os.environ["GITHUB_SHA"]
    else:
        branch_head = git("rev-parse", "HEAD")
    return main_head, branch_head


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True).stdout.strip()


if __name__ == "__main__":
    sys.exit(main())
