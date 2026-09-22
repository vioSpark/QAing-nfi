from __future__ import annotations

import json
import re
from pathlib import Path

from point import Point
from result import VerificationResult
from work_area_rectangle import WorkAreaRectangle

_POINT_RE = re.compile(r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)")


def parse_point(text: str) -> Point | None:
    match = _POINT_RE.search(text)
    if not match:
        return None
    return Point(float(match.group(1)), float(match.group(2)))


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
            corners.extend(Point(float(x), float(y)) for x, y in _POINT_RE.findall(line))
        elif section == "points":
            expected.extend(Point(float(x), float(y)) for x, y in _POINT_RE.findall(line))
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
    Path(path).write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
