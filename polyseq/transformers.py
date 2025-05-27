import itertools
import math

def tr_translate(poly: tuple[tuple[float, float], ...],
                 dx: int |float, dy: int |float) -> tuple[tuple[float, float], ...]:
    """
    Параллельный перенос многоугольника по осям координат на заданные значения.

    Аргументы:
        poly: Кортеж вершин многоугольника; каждая вершина — кортеж координат (float, float).
        dx: Смещение по оси x.
        dy: Смещение по оси y.

    Возвращает:
        Новый кортеж вершин многоугольника после сдвига.
    """
    if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
        raise TypeError('dx and dy must be numerical values (int or float)')

    return tuple(map(lambda vertex: (vertex[0] + dx, vertex[1] + dy), poly))

def tr_rotate(poly: tuple[tuple[float, float], ...],
              angle: int | float) -> tuple[tuple[float, float], ...]:
    """
    Поворот многоугольника на заданный угол.
    Важно: при применении к последовательности правильных многоугольников с помощью map() поворачивает
    не каждый отдельный многоугольник, а всю "ленту" сразу.

    Аргументы:
        poly: Кортеж вершин многоугольника; каждая вершина — кортеж координат (float, float).
        angle: угол поворота.

    Возвращает:
        Новый кортеж вершин многоугольника после поворота.
    """
    if not isinstance(angle, (int, float)):
        raise TypeError('angle must be a numerical value (int or float)')

    angle = math.radians(angle)
    return tuple(map(lambda vertex: (vertex[0]*math.cos(angle) - vertex[1]*math.sin(angle),
                                      vertex[0]*math.sin(angle) + vertex[1]*math.cos(angle)), poly))


_SYMMETRY = {
    'x': lambda vertex: (vertex[0], -vertex[1]), 0: lambda vertex: (vertex[0], -vertex[1]),
    'y': lambda vertex: (-vertex[0], vertex[1]), 1: lambda vertex: (-vertex[0], vertex[1])
}

def tr_symmetry(poly: tuple[tuple[float, float], ...],
                axis: int | str) -> tuple[tuple[float, float], ...]:
    """
    Симметричное отражение многоугольника относительно одной из осей.

    Аргументы:
        poly: Кортеж вершин многоугольника; каждая вершина — кортеж координат (float, float).
        axis: Ось симметрии. Ось абсцисс обозначается как 0 или 'x', ось ординат – 1 или 'y'.

    Возвращает:
        Новый кортеж вершин многоугольника после симметричного отражения.
    """
    try:
        flip = _SYMMETRY[axis]
    except KeyError as e:
        raise ValueError('incorrect axis indicator') from e

    return tuple(map(flip, poly))

def tr_homothety(poly: tuple[tuple[float, float], ...],
                 center: tuple[int | int] | tuple[float, float],
                 k: int | float) -> tuple[tuple[float, float], ...]:
    """
    Гомотетия плоскости с заданным центром и коэффициентом.

    Аргументы:
        poly: Кортеж вершин многоугольника; каждая вершина — кортеж координат (float, float)
        center: Центр гомотетии
        k: Коэффициент гомотетии. При k > 1 — растягивает, 0 < k < 1 — сжимает,
           k < 0 — инвертирует относительно центра.
           При к = 0 фигура вырождается в точку, поэтому в этом случае вызывается ValueError.

    Возвращает:
        Новый кортеж вершин многоугольника после гомотетии.
    """
    if not isinstance(center[0], (int, float)) or not isinstance(center[1], (int, float)):
        raise TypeError('center must be a 1-dimensional tuple of 2 numerical values (int or float)')

    if not isinstance(k, (int, float)):
        raise TypeError('k must be a numerical value (int or float)')

    if k == 0:
        raise ValueError

    a, b = center
    return tuple(map(lambda v: (k*(v[0] - a) + a, k*(v[1] - b) + b), poly))