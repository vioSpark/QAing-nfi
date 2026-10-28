"""Coverage protection policy: a branch may not have lower line coverage than main.

Compares two commits: main_head (the latest commit on main) and branch_head (the head of the branch under test).
Both are measured the same way, each in its own temporary checkout, with this checkout's coverage settings.
A partly covered line (it ran, but not every branch from it was taken) counts as not covered.

Usage, from the repository root:  python tools/coverage_protection_policy.py
Exit code 0 when the branch passes, 1 when it is rejected.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
from pathlib import Path

MAIN_REF = "origin/main"
TEST_PATH = "Create automated test"
COVERAGE_CONFIG = Path(".coveragerc").resolve()


def main() -> int:
    main_head, branch_head = identify_commit_pair()
    main_coverage = calculate_coverage(main_head)
    branch_coverage = calculate_coverage(branch_head)
    print(f"main_head   {main_head[:7]}: {main_coverage:.2f}% line coverage")
    print(f"branch_head {branch_head[:7]}: {branch_coverage:.2f}% line coverage")
    if branch_coverage < main_coverage:
        print("Coverage protection policy: REJECTED, line coverage went down")
        return 1
    print("Coverage protection policy: passed")
    return 0


def identify_commit_pair() -> tuple[str, str]:
    """main_head is the latest commit on main. branch_head is the pull request's head on a pull_request event,
    the dispatched commit on a workflow_dispatch, and HEAD when run locally."""
    main_head = git("rev-parse", MAIN_REF)
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        branch_head = event["pull_request"]["head"]["sha"]
    elif event_name == "workflow_dispatch":
        branch_head = os.environ["GITHUB_SHA"]
    else:
        branch_head = git("rev-parse", "HEAD")
    return main_head, branch_head


def calculate_coverage(commit: str) -> float:
    """Line coverage of one commit, in percent, from running its tests under coverage in a temporary checkout.

    Both commits use this checkout's .coveragerc (main may not have one yet), set once through COVERAGE_RCFILE so
    that every coverage command sees it. Failing tests don't stop the measurement: the test step judges the tests.
    """
    with tempfile.TemporaryDirectory() as temporary_folder:
        checkout = Path(temporary_folder) / "checkout"
        git("worktree", "add", "--detach", str(checkout), commit)
        try:
            environment = dict(os.environ, COVERAGE_RCFILE=str(COVERAGE_CONFIG))
            subprocess.run([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q", TEST_PATH],
                           cwd=checkout, env=environment)
            subprocess.run([sys.executable, "-m", "coverage", "xml", "-q", "-o", "coverage.xml"],
                           cwd=checkout, env=environment, check=True)
            return line_coverage(checkout / "coverage.xml")
        finally:
            git("worktree", "remove", "--force", str(checkout))


def line_coverage(cobertura_path: Path) -> float:
    """Fully covered lines / coverable lines, in percent, from a Cobertura file.

    Cobertura's own line-rate counts a partly covered line as covered, so it is not used. Only class-level lines
    are read: some tools repeat them at method level.
    """
    coverable_lines = fully_covered_lines = 0
    for line in ElementTree.parse(cobertura_path).getroot().iterfind("packages/package/classes/class/lines/line"):
        coverable_lines += 1
        ran = int(line.get("hits")) > 0
        all_branches_taken = line.get("branch") != "true" or line.get("condition-coverage", "").startswith("100%")
        if ran and all_branches_taken:
            fully_covered_lines += 1
    return 100 * fully_covered_lines / coverable_lines


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True).stdout.strip()


if __name__ == "__main__":
    sys.exit(main())
