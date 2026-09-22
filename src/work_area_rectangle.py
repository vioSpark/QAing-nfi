from __future__ import annotations

from point import Point


class WorkAreaRectangle:
    # Based on existing I/O files the arm seems accurate at 0.01-precision coordinates, but a 3rd
    # decimal digit seems to cause out-of-bound issues. For testing we use 0.0 accuracy; this likely
    # needs refinement from measurement data / robot-arm documentation review.
    def __init__(self, corners: list[Point], tolerance: float = 0.0) -> None:
        xs = sorted({c.x for c in corners})
        ys = sorted({c.y for c in corners})
        combos = {(c.x, c.y) for c in corners}
        if len(corners) != 4 or len(xs) != 2 or len(ys) != 2 or combos != {(x, y) for x in xs for y in ys}:
            raise ValueError(f"The working area's corners do not form an axis-aligned rectangle: {[str(c) for c in corners]}")
        self.min_x, self.max_x = xs
        self.min_y, self.max_y = ys
        self.tolerance = tolerance

    def is_inside(self, point: Point) -> bool:
        # There are no exact specs, but based on the input file it is expected for the robot to travel
        # to the edge of the work area. Therefore the edge counts as in (closed boundary, not open).
        t = self.tolerance
        return (self.min_x - t <= point.x <= self.max_x + t
                and self.min_y - t <= point.y <= self.max_y + t)
