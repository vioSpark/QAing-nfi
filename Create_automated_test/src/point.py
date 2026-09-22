from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self._format_coordinate(self.x)}, {self._format_coordinate(self.y)})"

    @staticmethod
    def _format_coordinate(value: float) -> str:
        # Drop the redundant ".0" on whole numbers so "(4, 150)" prints instead of "(4.0, 150.0)".
        return str(int(value)) if value == int(value) else str(value)
