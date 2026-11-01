from io_utils import parse_points
from point import Point


def test_parse_points_finds_every_point_on_a_line():
    assert parse_points("(-4, -150) (-4, 150) (160, -150)") == [Point(-4, -150), Point(-4, 150), Point(160, -150)]


def test_parse_points_skips_what_is_not_a_point():
    assert parse_points("(1, 2) (x, y) (3, 4") == [Point(1, 2)]   # unparsable, then unclosed
    assert parse_points("1, 2) (3, 4)") == [Point(3, 4)]          # closing bracket without an opening one
    assert parse_points("no points here") == []
