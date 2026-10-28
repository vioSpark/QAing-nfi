"""Coverage protection policy: a branch may not have lower line coverage than main.

Compares two Cobertura files: the coverage of main_head (the latest commit on main) and of branch_head (the head
of the branch under test), both measured with the branch's coverage settings. A partly covered line (it ran, but
not every branch from it was taken) counts as not covered.

Usage:  python tools/coverage_protection_policy.py <main_head coverage.xml> <branch_head coverage.xml>
Exit code 0 when the branch passes, 1 when it is rejected.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path


def main(arguments: list[str]) -> int:
    main_cobertura, branch_cobertura = (Path(argument) for argument in arguments)
    main_coverage = line_coverage(main_cobertura)
    branch_coverage = line_coverage(branch_cobertura)
    print(f"main_head:   {main_coverage:.2f}% line coverage")
    print(f"branch_head: {branch_coverage:.2f}% line coverage")
    if branch_coverage < main_coverage:
        print("Coverage protection policy: REJECTED, line coverage went down")
        return 1
    print("Coverage protection policy: passed")
    return 0


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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
