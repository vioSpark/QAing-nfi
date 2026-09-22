from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from io_utils import read_input_file, read_output_file, write_test_results
from point import Point
from result import VerificationResult
from work_area_rectangle import WorkAreaRectangle

_ROOT = Path(__file__).resolve().parent.parent
_SAMPLE_DIR = (_ROOT / "Nearfield Instruments Assignment_Software_Test_Engineer"
               / "Assignment_QA_Engineer" / "Assignment_QA_Engineer")
_DEFAULT_INPUT = _SAMPLE_DIR / "system_input_file.1630412935.txt"
_DEFAULT_OUTPUT = _SAMPLE_DIR / "system_ouput_file.1630412935.txt"
_DEFAULT_RESULTS = _ROOT / "test_results.txt"


def _same_point(a: Point, b: Point, tolerance: float) -> bool:
    return (math.isclose(a.x, b.x, rel_tol=0.0, abs_tol=tolerance)
            and math.isclose(a.y, b.y, rel_tol=0.0, abs_tol=tolerance))


def verify(work_area: WorkAreaRectangle, expected: list[Point], actual: list[Point],
           warnings: list[str], input_file: str, output_file: str) -> VerificationResult:
    failures: list[str] = []
    tol = work_area.tolerance

    for point in actual:
        if not work_area.is_inside(point):
            failures.append(f"Req 2: actual point {point} is outside the work area")

    for point in expected:
        if not work_area.is_inside(point):
            warnings.append(f"Expected input point {point} is outside the work area")
            continue
        if not any(_same_point(point, a, tol) for a in actual):
            failures.append(f"Coverage: expected point {point} was never visited")

    work_area_dict = {
        "x": [work_area.min_x, work_area.max_x],
        "y": [work_area.min_y, work_area.max_y],
        "tolerance": tol,
    }
    return VerificationResult(expected=expected, actual=actual, work_area=work_area_dict,
                              input_file=input_file, output_file=output_file,
                              failures=failures, warnings=warnings)


def _report(result: VerificationResult, results_path: str) -> None:
    for warning in result.warnings:
        print(f"WARN: {warning}")
    if result.passed:
        print(f"PASS - all requirements met. Results written to {results_path}")
        return
    print(f"FAIL - {len(result.failures)} requirement violation(s):")
    for failure in result.failures:
        print(f"  - {failure}")
    print(f"Results written to {results_path}")


def _finish(result: VerificationResult, results_path: str) -> int:
    write_test_results(result, results_path)
    _report(result, results_path)
    return 0 if result.passed else 1


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify robot-arm movement against work-area requirements.")
    parser.add_argument("--input", default=str(_DEFAULT_INPUT))
    parser.add_argument("--output", default=str(_DEFAULT_OUTPUT))
    parser.add_argument("--results", default=str(_DEFAULT_RESULTS))
    parser.add_argument("--tolerance", type=float, default=0.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        work_area, expected = read_input_file(args.input, args.tolerance)
    except (OSError, ValueError) as exc:
        result = VerificationResult(expected=[], actual=[],
                                    work_area={"x": None, "y": None, "tolerance": args.tolerance},
                                    input_file=args.input, output_file=args.output,
                                    failures=[f"Req 1: cannot read expected points from input. {exc}"])
        return _finish(result, args.results)

    try:
        actual, warnings = read_output_file(args.output)
    except OSError as exc:
        result = VerificationResult(expected=expected, actual=[],
                                    work_area={"x": [work_area.min_x, work_area.max_x],
                                               "y": [work_area.min_y, work_area.max_y],
                                               "tolerance": work_area.tolerance},
                                    input_file=args.input, output_file=args.output,
                                    failures=[f"Req 3: cannot read actual points from output. {exc}"])
        return _finish(result, args.results)

    result = verify(work_area, expected, actual, warnings, args.input, args.output)
    return _finish(result, args.results)


if __name__ == "__main__":
    sys.exit(main())
