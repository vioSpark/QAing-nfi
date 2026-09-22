from __future__ import annotations

import json
from pathlib import Path

from point import Point
from verification_result import VerificationResult
from work_area_rectangle import WorkAreaRectangle


def parse_point(text: str) -> Point | None:
    text = text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        return None
    parts = text[1:-1].split(",")
    if len(parts) != 2:
        return None
    try:
        return Point(float(parts[0]), float(parts[1]))
    except ValueError:
        return None


def parse_points(line: str) -> list[Point]:
    points: list[Point] = []
    start: int | None = None
    for i, char in enumerate(line):
        if char == "(":
            start = i
        elif char == ")" and start is not None:
            point = parse_point(line[start:i + 1])
            if point is not None:
                points.append(point)
            start = None
    return points


def read_input_file(path: str, tolerance: float = 0.0) -> tuple[WorkAreaRectangle, list[Point]]:
    corners: list[Point] = []
    expected: list[Point] = []
    section: str | None = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low == "rectangle":
            section = "rectangle"
        elif low == "points":
            section = "points"
        elif section == "rectangle":
            corners.extend(parse_points(line))
        elif section == "points":
            expected.extend(parse_points(line))
    if not corners:
        raise ValueError(f"No 'Rectangle' corners found in input file: {path}")
    if not expected:
        raise ValueError(f"No 'Points' found in input file: {path}")
    return WorkAreaRectangle(corners, tolerance), expected


def read_output_file(path: str) -> tuple[list[Point], list[str]]:
    actual: list[Point] = []
    warnings: list[str] = []
    for lineno, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        point = parse_point(line)
        if point is None:
            warnings.append(f"Output line {lineno} {line!r} ignored (homing / log noise)")
        else:
            actual.append(point)
    return actual, warnings


def write_test_results(result: VerificationResult, path: str) -> None:
    lines = ["# Expected visited points"]
    lines += [str(p) for p in result.expected]
    lines.append("# Actual visited points")
    lines += [str(p) for p in result.actual]
    lines.append("# Test result")
    lines.append(result.result)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_test_results_json(result: VerificationResult, path: str) -> None:
    Path(path).write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
