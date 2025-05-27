import itertools
import functools
import math

def _pseudo_scalar_prod(vec1, vec2) -> float:
    """Псевдоскалярное произведение двух векторов в ортонормированном базисе (2-d dot product)."""
    x1, y1 = vec1
    x2, y2, = vec2
    return x1*y2 - y1*x2

def _area(poly: tuple[tuple[float, float], ...]) -> float:
    """Формула площади Гаусса (алгоритм шнурования)."""
    n = len(poly)
    return 0.5*abs(sum(
        (poly[i][0]*poly[(i+1) % n][1] - poly[(i+1) % n][0]*poly[i][1])
        for i in range(n)))


def flt_convex_polygon(poly: tuple[tuple[float, float], ...]) -> bool:
    """
    Проверка выпуклости многоугольника.

    Алгоритм: для каждой пары соседних рёбер вычисляем знак
    псевдоскалярного произведения. Если знаки меняются — есть перегиб,
    значит многоугольник невыпуклый.
    """
    sign = 0
    for k in range(len(poly)):
        side = (poly[(k+1) % len(poly)][0] - poly[k][0], poly[(k+1) % len(poly)][1] - poly[k][1])
        next_side = (poly[(k+2) % len(poly)][0] - poly[(k+1) % len(poly)][0], poly[(k+2) % len(poly)][1] - poly[(k+1) % len(poly)][1])

        p = _pseudo_scalar_prod(side, next_side)
        if p:
            if sign == 0:
                sign = 1 if p > 0 else -1
            elif sign * p < 0:
                return False
    return True


def flt_vertex_point(poly, point):
    """Проверяет совпадение заданной точки с одной из сторон многоугольника."""
    return point in poly

def flt_area_lt(poly: tuple[tuple[float, float], ...],
                area: int | float) -> bool:
    """Проверяет, является ли площадь многоугольника меньше заданного значения."""
    return _area(poly) < area

def flt_shortest_side_lt(poly: tuple[tuple[float, float], ...],
                         shortest_side: int | float) -> bool:
    """Проверяет, является ли кратчайшая сторона многоугольника меньше заданного значения."""
    return min(map(lambda i: math.dist(poly[i], poly[(i+1) % len(poly)]), range(len(poly)))) < shortest_side

def flt_point_inside(poly: tuple[tuple[float, float], ...],
                     point: tuple[float, float]) -> bool:
    """
    Проверяет, принадлежит ли точка выпуклому многоугольнику.

    Алгоритм: для каждого ребра вычисляется знак псевдоскалярного
    произведения (2-d cross-product) вектора ребра и вектора «вершина → точка».
    Если знаки совпадают (или ноль — точка на ребре) для всех рёбер,
    точка лежит внутри или на границе.
    """

    if not flt_convex_polygon(poly):
        return False

    n = len(poly)
    sign = 0
    for k in range(n):
        side = (poly[(k + 1) % n][0] - poly[k][0],
                poly[(k + 1) % n][1] - poly[k][1])
        vertex_to_point_vec = (point[0] - poly[k][0],
                               point[1] - poly[k][1])

        p = _pseudo_scalar_prod(side, vertex_to_point_vec)
        if p:
            if sign == 0:
                sign = 1 if p > 0 else -1
            elif sign * p < 0:
                return False
    return True


def flt_polygon_vertices(poly: tuple[tuple[float, float], ...],
                              base) -> bool:
    """Проверяет, совпадение хотя бы одной вершины многоугольника с данной фигурой."""
    return bool(set(base) & set(poly))