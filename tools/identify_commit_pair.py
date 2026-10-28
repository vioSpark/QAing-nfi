"""Identify the commits for the coverage protection policy: main_head, branch_head and merge_commit.

The policy compares main_head with the result of merging branch_head into it.
- pull_request: merge_commit is the merge commit GitHub made for the pull request (GITHUB_SHA), main_head is its
  first parent (the main commit it merges onto) and branch_head is the pull request's head.
- workflow_dispatch, and locally: main_head is the latest commit on main, branch_head is the dispatched commit
  (locally HEAD), and merge_commit is empty: the coverage job merges main_head into branch_head itself.

Usage, from the repository root:  python tools/identify_commit_pair.py
Prints main_head=, branch_head= and merge_commit= lines, and appends them to $GITHUB_OUTPUT when it is set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    main_head, branch_head, merge_commit = identify_commit_pair()
    outputs = f"main_head={main_head}\nbranch_head={branch_head}\nmerge_commit={merge_commit}\n"
    print(outputs, end="")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output_file:
            output_file.write(outputs)
    return 0


def identify_commit_pair() -> tuple[str, str, str]:
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        merge_commit = os.environ["GITHUB_SHA"]
        main_head = git("rev-parse", f"{merge_commit}^1")
        branch_head = event["pull_request"]["head"]["sha"]
        return main_head, branch_head, merge_commit
    main_head = git("ls-remote", "origin", "refs/heads/main").split()[0]
    branch_head = os.environ["GITHUB_SHA"] if event_name == "workflow_dispatch" else git("rev-parse", "HEAD")
    return main_head, branch_head, ""


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True).stdout.strip()


if __name__ == "__main__":
    sys.exit(main())
