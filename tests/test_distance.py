from src.distance import euclidean_distance
from src.models import Point


def test_3_4_5_triangle():
    assert euclidean_distance(Point(0, 0), Point(3, 4)) == 5.0


def test_same_point_is_zero():
    p = Point(7, 2)
    assert euclidean_distance(p, p) == 0.0


def test_symmetric():
    a, b = Point(1, 1), Point(4, 5)
    assert euclidean_distance(a, b) == euclidean_distance(b, a)


def test_negative_coordinates():
    assert euclidean_distance(Point(-3, -4), Point(0, 0)) == 5.0
