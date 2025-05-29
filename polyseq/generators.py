import itertools
import math
from typing import Iterator
from polyseq.transformers import tr_translate, tr_rotate
import random
from polyseq.visualization import visualize
import matplotlib.pyplot as plt

def _regular_polygon(n_sides, l: int = 1) -> tuple[tuple[float, float], ...]:
    """
    Генерирует вершины правильного многоугольника с центром в начале координат.
    Каждая вершина вычисляется исходя из того, что многоугольник вписан в окружность,
    радиус которой рассчитывается на основе длины стороны.

    Аргументы:
        n_sides: Количество сторон (вершин) многоугольника. Должно быть >= 3.
        l: Длина стороны многоугольника. По умолчанию 1.

    Возвращает:
        Кортеж из вершин размера (n_sides, 2); каждая вершина – кортеж (float, float).
    """
    radius = l / (2*math.sin(math.pi/n_sides))
    vertices = (
        (radius * math.cos(2*math.pi*k/n_sides),
        radius * math.sin(2*math.pi*k/n_sides))
        for k in range(n_sides)
    )
    return tuple(vertices)

def _random_polygon(n_sides: int | float | None = None) -> tuple[tuple[float, float], ...]:
    """
    Генерирует вершины случайного многоугольника.
    Если число сторон не указано, выбирается случайное число от 3 до 12 включительно.
    Вершины определяются случайными углами и радиусами относительно случайного центра

    Аргументы:
        n_sides: Количество сторон многоугольника.
            Если None, выбирается случайное число от 3 до 12. По умолчанию None.

    Возвращает:
        Кортеж из вершин размера (n_sides, 2) ;
        каждая вершина – кортеж координат (float, float).
    """
    center = (random.uniform(0,50), random.uniform(0,50))
    n_sides = random.randint(3,13) if n_sides is None else n_sides
    angles = tuple(sorted((random.uniform(0, 2*math.pi) for _ in range(n_sides))))
    radiuses = tuple(random.uniform(0.1, 10) for _ in range(n_sides))
    vertices = ((radiuses[i]*math.cos(angles[i]) + center[0], radiuses[i]*math.sin(angles[i]) + center[1]) for i in range(n_sides))
    return tuple(vertices)


def gen_reg_polygon_seq(n_sides: int, step: int | float = 1, n_figs: int | float = math.inf,
                 l: int | float = 1) -> Iterator[tuple[tuple[float, float], ...]]:
    """
    Генерирует конечную или бесконечную последовательность правильных
    многоугольников с заданным количеством сторон.
    Каждый многоугольник последовательности – "базовый" многоугольник с центром в
    (0,0), смещенный на его ширину + шаг.

    Аргументы:
        n_sides: Количество сторон правильного многоугольника. Должно быть не меньше 3.
        step: Расстояние между многоугольниками по оси X. По умолчанию 1.
        n_figs: Количество многоугольников для генерации.
            Если math.inf — генератор бесконечен. По умолчанию бесконечность.
        l: Длина стороны каждого многоугольника. По умолчанию 1.

    Возвращает:
        Итератор, генерирующий кортежи из вершин размера (n_sides, 2);
        каждая вершина – кортеж координат (float, float)

    Исключения:
        TypeError: Если типы аргументов не соответствуют ожидаемым.
        ValueError: Если количество сторон меньше 3 или n_figs не целое число и не бесконечность.
    """

    if not isinstance(n_sides, int):
        raise TypeError('step must be a whole numerical value (int or float)')
    
    if not isinstance(step, (int, float)):
        raise TypeError('step must be a numerical value (int or float)')

    if not isinstance(n_figs, (int, float)):
        raise TypeError('n_figs must either be whole a numerical value (int or float) or math.inf')

    if not isinstance(l, (int, float)):
        raise TypeError('l must be a numerical value (int or float)')

    if n_sides < 3:
        raise ValueError('n_sides must be greater or equal to 3')

    if not n_figs.is_integer() and not math.isinf(n_figs):
        raise ValueError('n_figs cannot be a fraction')

    base_poly = tr_rotate(_regular_polygon(n_sides, l=l), 90) if n_sides != 4 \
        else tr_rotate(_regular_polygon(n_sides, l=l), 45)
    x_cords = tuple(map(lambda p: p[0], base_poly))
    x_shift = max(x_cords) - min(x_cords) + step
    stream = map(lambda shift: tr_translate(base_poly, shift, 0), itertools.count(0, x_shift))
    if math.isinf(n_figs):
        yield from stream
    else:
        yield from itertools.islice(stream, n_figs)


def gen_random_polygon_seq(n_figs: int | float,
                           n_sides: int | float | None = None) -> Iterator[tuple[tuple[float], float, ...]]:
    """
    Генерирует конечную последовательность случайных многоугольников.

    Аргументы:
        n_figs: Количество многоугольников для генерации.
        n_sides: Количество сторон случайного многоугольника. Если None, выбирается случайное количество сторон.
        Может умолчанию None.

    Возвращает:
        Итератор, генерирующий кортежи из вершин размера (n_sides, 2);
        каждая вершина – кортеж координат (float, float)

    Исключения:

    """
    if not isinstance(n_figs, (int, float)):
        raise TypeError('n_figs must be a whole numerical value (int or float)')

    if n_sides is not None and not isinstance(n_sides, (int, float)):
        raise TypeError('n_sides must be a whole numerical value (int or float)')

    if n_sides is not None and n_sides < 3:
        raise ValueError('n_sides must be greater or equal to 3')

    if n_figs is not None and not n_figs.is_integer():
        raise ValueError('n_figs cannot be a fraction')

    if n_sides is not None and not n_sides.is_integer():
        raise ValueError('n_sides cannot be a fraction')

    yield from (_random_polygon(n_sides) for _ in range(n_figs))

