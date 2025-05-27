import math
import pytest

from polyseq.filters import (
    _pseudo_scalar_prod,
    _area,
    flt_convex_polygon,
    flt_vertex_point,
    flt_area_lt,
    flt_shortest_side_lt,
    flt_point_inside,
    flt_polygon_vertices,
)


# Простые тестовые многоугольники
SQUARE = ((0,0), (1,0), (1,1), (0,1))
NON_CONVEX = ((0,0), (2,0), (1,1), (2,2), (0,2))
TRIANGLE = ((0,0), (2,0), (1,1.732))  # правильный треугольник


# ───── _pseudo_scalar_prod ─────
def test_pseudo_scalar_prod_sign():
    # Ортогональные векторы должны давать положительное/отрицательное значение
    v1 = (1, 0)
    v2 = (0, 1)
    assert _pseudo_scalar_prod(v1, v2) > 0

    v3 = (0, -1)
    assert _pseudo_scalar_prod(v1, v3) < 0


# ───── _area ─────
def test_area_square():
    assert math.isclose(_area(SQUARE), 1.0, rel_tol=1e-9)

def test_area_triangle():
    expected = 0.5 * 2 * 1.732  # 0.5 * base * height
    assert math.isclose(_area(TRIANGLE), expected, rel_tol=1e-9)


# ───── flt_convex_polygon ─────
def test_flt_convex_polygon_positive():
    assert flt_convex_polygon(SQUARE) is True
    assert flt_convex_polygon(TRIANGLE) is True

def test_flt_convex_polygon_negative():
    assert flt_convex_polygon(NON_CONVEX) is False


# ───── flt_vertex_point ─────
def test_flt_vertex_point_true():
    assert flt_vertex_point(SQUARE, (1,0)) is True

def test_flt_vertex_point_false():
    assert flt_vertex_point(SQUARE, (0.5, 0)) is False


# ───── flt_area_lt ─────
def test_flt_area_lt_true():
    assert flt_area_lt(SQUARE, 2.0) is True

def test_flt_area_lt_false():
    assert flt_area_lt(SQUARE, 0.5) is False


# ───── flt_shortest_side_lt ─────
def test_flt_shortest_side_lt_true():
    # Кратчайшая сторона квадрата = 1
    assert flt_shortest_side_lt(SQUARE, 1.1) is True

def test_flt_shortest_side_lt_false():
    assert flt_shortest_side_lt(SQUARE, 0.9) is False


# ───── flt_point_inside ─────
def test_flt_point_inside_inside():
    # Точка внутри квадрата
    assert flt_point_inside(SQUARE, (0.5, 0.5)) is True

def test_flt_point_inside_outside():
    # Точка снаружи квадрата
    assert flt_point_inside(SQUARE, (1.5, 1.5)) is False

def test_flt_point_inside_on_edge():
    # Точка на ребре
    assert flt_point_inside(SQUARE, (0.5, 0)) is True

def test_flt_point_inside_nonconvex_false():
    # Для невыпуклого полигона функция должна вернуть False
    assert flt_point_inside(NON_CONVEX, (1.5, 0.5)) is False


# ───── flt_polygon_vertices ─────
def test_flt_polygon_vertices_true():
    base = ((0,0), (1,1))
    poly = ((0,0), (2,2), (3,3))
    assert flt_polygon_vertices(poly, base) is True

def test_flt_polygon_vertices_false():
    base = ((0,0), (1,1))
    poly = ((2,2), (3,3), (4,4))
    assert flt_polygon_vertices(poly, base) is False
