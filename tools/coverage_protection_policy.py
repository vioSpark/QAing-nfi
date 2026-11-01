"""Coverage protection policy: merging a branch into main may not lower line coverage, unless it is saturated.

Compares two Cobertura files: the coverage of main_head and of the merge of branch_head into main_head, both
measured with the branch's coverage settings. A partly covered line (it ran, but not every branch from it was
taken) counts as not covered. At or above the saturation level the merge may lower line coverage.

Usage:  python tools/coverage_protection_policy.py <main_head coverage.xml> <merge coverage.xml>
Exit code 0 when the branch passes, 1 when it is rejected.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

# Line coverage in percent. Chasing the last few percent is rarely worth a blocked pull request.
SATURATION_LEVEL = 95.0


def main(arguments: list[str]) -> int:
    main_cobertura, merge_cobertura = (Path(argument) for argument in arguments)
    main_coverage = line_coverage(main_cobertura)
    merge_coverage = line_coverage(merge_cobertura)
    print(f"{'main_head:':<35}{main_coverage:.2f}% line coverage")
    print(f"{'branch_head merged into main_head:':<35}{merge_coverage:.2f}% line coverage")
    print(f"{'saturation level:':<35}{SATURATION_LEVEL:.2f}% line coverage")
    # Line coverage may not decrease: equal passes.
    if main_coverage <= merge_coverage:
        print("Coverage protection policy: passed")
        return 0
    # Saturated: the merge may lower line coverage as long as it stays at or above the saturation level.
    if merge_coverage >= SATURATION_LEVEL:
        print("Coverage protection policy: passed, line coverage went down but stays saturated")
        return 0
    print("Coverage protection policy: REJECTED, line coverage went down below the saturation level")
    return 1


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
