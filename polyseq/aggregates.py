import math

def _sides(poly):
    """Возвращает длины рёбер многоугольника в виде кортежа."""
    n = len(poly)
    return tuple(
        math.dist(poly[i], poly[(i + 1) % n])
        for i in range(n)
    )
def _area(poly: tuple[tuple[float, float], ...]) -> float:
    """Формула площади Гаусса (алгоритм шнурования)."""
    n = len(poly)
    return 0.5*abs(sum(
        (poly[i][0]*poly[(i+1) % n][1] - poly[(i+1) % n][0]*poly[i][1])
        for i in range(n)))

def agr_origin_nearest(polygon_seq):
    """Минимальное расстояние от начала координат до любой вершины всех многоугольников."""
    return min(min(math.dist(point, (0, 0)) for point in poly) for poly in polygon_seq)

def agr_max_side(polygon_seq):
    """Максимальная длина стороны среди всех многоугольников."""
    return max(map(max, map(_sides, polygon_seq)))

def agr_min_area(polygon_seq):
    """Минимальная площадь среди всех многоугольников."""
    return min(map(_area, polygon_seq))

def agr_perimeter(polygon_seq):
    """Суммарный периметр всех многоугольников из последовательности."""
    return sum(map(lambda poly: sum(_sides(poly)), polygon_seq))

def agr_area(polygon_seq):
    """Суммарная площадь всех многоугольников из последовательности."""
    return sum(map(_area, polygon_seq))