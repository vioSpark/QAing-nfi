from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self._fmt(self.x)}, {self._fmt(self.y)})"

    @staticmethod
    def _fmt(value: float) -> str:
        return str(int(value)) if value == int(value) else str(value)
