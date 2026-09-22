import pytest

from io_utils import parse_point
from main import verify
from point import Point
from work_area_rectangle import WorkAreaRectangle


def rect(tolerance: float = 0.0) -> WorkAreaRectangle:
    corners = [Point(-4, -150), Point(-4, 150), Point(160, -150), Point(160, 150)]
    return WorkAreaRectangle(corners, tolerance)


def test_point_str_formats_int_and_float():
    assert str(Point(160.0, -150.0)) == "(160, -150)"
    assert str(Point(-4.23, -150.56)) == "(-4.23, -150.56)"
    assert str(Point(0.045, 0.001)) == "(0.045, 0.001)"


def test_rectangle_rejects_non_rectangle():
    with pytest.raises(ValueError):
        WorkAreaRectangle([Point(0, 0), Point(0, 1), Point(1, 0), Point(2, 2)])
    with pytest.raises(ValueError):
        WorkAreaRectangle([Point(0, 0), Point(0, 1), Point(1, 0)])


def test_is_inside_closed_boundary():
    r = rect()
    assert r.is_inside(Point(0, 0))
    assert r.is_inside(Point(4, 150))      # on edge
    assert r.is_inside(Point(-4, -150))    # corner
    assert r.is_inside(Point(160, -150))   # corner
    assert not r.is_inside(Point(170, 150))
    assert not r.is_inside(Point(-4.23, -150.56))


def test_tolerance_zero_is_exact_edge():
    assert not rect(0.0).is_inside(Point(160.001, 0))


def test_tolerance_expands_boundary():
    assert rect(0.01).is_inside(Point(160.01, 0))
    assert not rect(0.01).is_inside(Point(160.02, 0))


def test_parse_point_variants():
    assert parse_point("(160.00, -150.00)") == Point(160, -150)
    assert parse_point("(-3, -149)") == Point(-3, -149)
    assert parse_point("(0.045, 0.001)") == Point(0.045, 0.001)
    assert parse_point("error") is None
    assert parse_point("()") is None
    assert parse_point("") is None


def test_verify_flags_out_of_bounds_and_coverage():
    expected = [Point(-3, -149), Point(0.045, 0.001), Point(170, 150)]
    actual = [Point(-3, -149), Point(0, 0), Point(170, 150)]
    result = verify(rect(), expected, actual, [], "in", "out")
    assert result.result == "FAIL"
    assert any("outside the work area" in f for f in result.failures)   # actual (170, 150)
    assert any("never visited" in f for f in result.failures)           # expected (0.045, 0.001)
    assert any("Expected input point (170, 150)" in w for w in result.warnings)


def test_verify_passes_clean_run():
    expected = [Point(-3, -149), Point(4, 150)]
    actual = [Point(-3, -149), Point(4, 150), Point(0, 0)]   # extra in-bounds home is fine
    result = verify(rect(), expected, actual, [], "in", "out")
    assert result.result == "PASS"
    assert result.failures == []
