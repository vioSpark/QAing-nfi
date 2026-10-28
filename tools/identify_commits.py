"""Identify the commits for the coverage protection policy: main_head, branch_head and merge_commit.

The policy compares main_head with merge_commit, the merge of branch_head into main_head.
- pull_request: merge_commit is the merge commit GitHub made for the pull request (GITHUB_SHA), main_head is its
  first parent (the main commit it merges onto) and branch_head is the pull request's head.
- workflow_dispatch, and locally: main_head is the latest commit on main, branch_head is the dispatched commit
  (locally HEAD), and merge_commit is created here (create_merge_commit.py).

Usage, from the repository root:  python tools/identify_commits.py
Prints main_head=, branch_head= and merge_commit= lines, and appends them to $GITHUB_OUTPUT when it is set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

from create_merge_commit import MergeConflict, create_merge_commit


class Commits(NamedTuple):
    main_head: str
    branch_head: str
    merge_commit: str


def main() -> int:
    try:
        commits = identify_commits()
    except MergeConflict as conflict:
        print(f"::error::branch_head has merge conflicts with main_head; resolve them first.\n{conflict}",
              file=sys.stderr)
        return 1
    outputs = "".join(f"{name}={sha}\n" for name, sha in commits._asdict().items())
    print(outputs, end="")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output_file:
            output_file.write(outputs)
    return 0


def identify_commits() -> Commits:
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        merge_commit = os.environ["GITHUB_SHA"]
        return Commits(main_head=git("rev-parse", f"{merge_commit}^1"),
                       branch_head=event["pull_request"]["head"]["sha"],
                       merge_commit=merge_commit)
    main_head = git("ls-remote", "origin", "refs/heads/main").split()[0]
    branch_head = os.environ["GITHUB_SHA"] if event_name == "workflow_dispatch" else git("rev-parse", "HEAD")
    # In principle not needed with pull_request, where GitHub makes the merge commit. Needed when the policy runs
    # without one: on a workflow_dispatch (CI usage optimizations) and locally.
    return Commits(main_head, branch_head, create_merge_commit(main_head, branch_head))


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True).stdout.strip()


if __name__ == "__main__":
    sys.exit(main())
