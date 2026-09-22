from __future__ import annotations

from dataclasses import dataclass, field

from point import Point


@dataclass
class VerificationResult:
    expected: list[Point]
    actual: list[Point]
    work_area: dict
    input_file: str
    output_file: str
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    @property
    def result(self) -> str:
        return "PASS" if self.passed else "FAIL"

    def to_dict(self) -> dict:
        return {
            "test_result": self.result,
            "expected_visited_points": [str(p) for p in self.expected],
            "actual_visited_points": [str(p) for p in self.actual],
            "work_area": self.work_area,
            "input_file": self.input_file,
            "output_file": self.output_file,
            "failures": self.failures,
            "warnings": self.warnings,
        }
