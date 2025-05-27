import math
import pytest

from polyseq.aggregates import (
    _sides,
    _area,
    agr_origin_nearest,
    agr_max_side,
    agr_min_area,
    agr_perimeter,
    agr_area,
)

SQUARE = ((0, 0), (1, 0), (1, 1), (0, 1))
RECTANGLE = ((0, 0), (3, 0), (3, 1), (0, 1))
TRIANGLE = ((0, 0), (3, 0), (1.5, 2))

# Тесты для _sides
def test_sides_square():
    sides = _sides(SQUARE)
    expected = (1, 1, 1, 1)
    for s, e in zip(sides, expected):
        assert math.isclose(s, e)

def test_sides_rectangle():
    sides = _sides(RECTANGLE)
    expected = (3, 1, 3, 1)
    for s, e in zip(sides, expected):
        assert math.isclose(s, e)

# Тесты для _area
def test_area_square():
    area = _area(SQUARE)
    assert math.isclose(area, 1.0)

def test_area_triangle():
    area = _area(TRIANGLE)
    expected = 0.5 * 3 * 2  # 3*2/2 = 3
    assert math.isclose(area, expected)

# Тесты для agr_origin_nearest
def test_agr_origin_nearest():
    polys = [SQUARE, RECTANGLE, TRIANGLE]
    res = agr_origin_nearest(polys)
    # Минимальное расстояние от (0,0) до вершин — это 0 (сама точка (0,0))
    assert math.isclose(res, 0)

# Тесты для agr_max_side
def test_agr_max_side():
    polys = [SQUARE, RECTANGLE]
    res = agr_max_side(polys)
    # максимальная сторона — 3 у RECTANGLE
    assert math.isclose(res, 3)

# Тесты для agr_min_area
def test_agr_min_area():
    polys = [SQUARE, RECTANGLE, TRIANGLE]
    res = agr_min_area(polys)
    # минимальная площадь — квадрат 1.0
    assert math.isclose(res, 1.0)

# Тесты для agr_perimeter
def test_agr_perimeter():
    polys = [SQUARE, RECTANGLE]
    res = agr_perimeter(polys)
    # Периметр квадрата: 4; Периметр прямоугольника: 8; сумма = 12
    assert math.isclose(res, 12)

# Тесты для agr_area
def test_agr_area():
    polys = [SQUARE, TRIANGLE]
    res = agr_area(polys)
    # Площадь квадрата 1 + площадь треугольника 3 = 4
    assert math.isclose(res, 4)
