"""Create the merge commit of branch_head into main_head, the way GitHub does for a pull request.

In principle this is not needed with pull_request: GitHub makes the merge commit itself. It is needed when the
policy runs without one: on a workflow_dispatch (CI usage optimizations, e.g. not running on every pull request
event) and locally.

The commit is reproducible: a fixed identity, branch_head's commit time and a fixed message, so every runner that
creates it from the same two commits gets the same SHA. It only adds objects to the repository; the working tree,
the index and HEAD stay as they are.

Usage, from the repository:  python tools/create_merge_commit.py <main_head> <branch_head>
Prints the merge commit's SHA. Exit code 1, with git's conflict report, when the two don't merge cleanly.
"""
from __future__ import annotations

import os
import subprocess
import sys

IDENTITY = {
    "GIT_AUTHOR_NAME": "Coverage protection policy",
    "GIT_AUTHOR_EMAIL": "noreply@github.com",
    "GIT_COMMITTER_NAME": "Coverage protection policy",
    "GIT_COMMITTER_EMAIL": "noreply@github.com",
}


class MergeConflict(Exception):
    pass


def main(arguments: list[str]) -> int:
    main_head, branch_head = arguments
    try:
        print(create_merge_commit(main_head, branch_head))
    except MergeConflict as conflict:
        print(f"::error::branch_head {branch_head} has merge conflicts with main_head {main_head}; "
              f"resolve them first.\n{conflict}", file=sys.stderr)
        return 1
    return 0


def create_merge_commit(main_head: str, branch_head: str) -> str:
    merge = subprocess.run(["git", "merge-tree", "--write-tree", main_head, branch_head],
                           capture_output=True, text=True)
    if merge.returncode == 1:
        raise MergeConflict(merge.stdout)
    merge.check_returncode()
    tree = merge.stdout.splitlines()[0]
    commit_time = git("show", "--no-patch", "--format=%ct", branch_head) + " +0000"
    environment = dict(os.environ, **IDENTITY, GIT_AUTHOR_DATE=commit_time, GIT_COMMITTER_DATE=commit_time)
    return git("commit-tree", tree, "-p", main_head, "-p", branch_head, "-m", f"Merge {branch_head} into {main_head}",
               environment=environment)


def git(*arguments: str, environment: dict[str, str] | None = None) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True,
                          env=environment).stdout.strip()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
