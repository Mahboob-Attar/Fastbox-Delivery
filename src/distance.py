"""A single, reusable distance function."""

import math

from .models import Point


def euclidean_distance(point1: Point, point2: Point) -> float:
    """Straight-line distance between two points."""
    return math.hypot(point2.x - point1.x, point2.y - point1.y)
