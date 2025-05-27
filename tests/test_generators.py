import math
import itertools
import random
import pytest

from polyseq.generators import (
    _regular_polygon,
    _random_polygon,
    gen_reg_polygon_seq,
    gen_random_polygon_seq,
)
from polyseq.transformers import tr_translate


# ─────────────────────────── фикстуры ────────────────────────────
@pytest.fixture(autouse=True)
def rng_seed():
    """
    Фикстура запускается ПЕРЕД каждым тестом (autouse=True)
    и фиксирует seed — все случайные величины будут воспроизводимы.
    """
    random.seed(42)


@pytest.fixture
def triangle():
    """Мини-треугольник со стороной 2."""
    return _regular_polygon(3, l=2)


# ─────────────────────────── тесты _regular_polygon ──────────────
def test_regular_polygon_side_length():
    """
    Проверяем, что расстояние между соседними вершинами равно заданной длине `l`
    (с поправкой на floating-point).
    """
    l = 5
    n = 6
    poly = _regular_polygon(n_sides=n, l=l)
    for i in range(n):
        d = math.dist(poly[i], poly[(i + 1) % n])
        assert math.isclose(d, l, rel_tol=1e-9)


def test_regular_polygon_center():
    """
    Сумма координат вершин для правильного многоугольника должна давать центр (0,0).
    """
    poly = _regular_polygon(5, l=1)
    cx = sum(v[0] for v in poly) / len(poly)
    cy = sum(v[1] for v in poly) / len(poly)
    assert math.isclose(cx, 0, abs_tol=1e-12)
    assert math.isclose(cy, 0, abs_tol=1e-12)


# ─────────────────────────── тесты gen_reg_polygon_seq ───────────
def test_reg_sequence_count_and_shift():
    """
    Проверяем:
    1. Генератор возвращает ровно `n_figs` элементов.
    2. Сдвиг между центрами соседних фигур равен ширине + step.
    """
    n_sides = 4
    n_figs  = 4
    step    = 2
    l       = 1

    seq = list(gen_reg_polygon_seq(n_sides, step=step, n_figs=n_figs, l=l))

    # 1) длина
    assert len(seq) == n_figs

    # 2) сдвиг: сравним x-координаты первой вершины
    base   = seq[0][0][0]
    second = seq[1][0][0]
    third  = seq[2][0][0]

    delta1 = second - base
    delta2 = third  - second
    exp_shift = max(map(lambda v: v[0], seq[0])) - min(map(lambda v: v[0], seq[0])) + step
    assert math.isclose(delta1, delta2)          # шаг постоянный
    assert math.isclose(delta1, exp_shift)       # ---


def test_reg_sequence_infinite_slice():
    """
    Бесконечную последовательность можно отбросить `islice`-ом —
    берём 10 первых элементов и убеждаемся, что это не падает.
    """
    it = itertools.islice(gen_reg_polygon_seq(3, step=1.5, n_figs=math.inf, l=1),
                          0, 10)
    polys = list(it)
    assert len(polys) == 10


# ─────────────────────────── тесты _random_polygon ───────────────
def test_random_polygon_sides_fixed():
    """
    Если передать `n_sides`, полигон должен содержать именно столько вершин.
    """
    poly = _random_polygon(n_sides=7)
    assert len(poly) == 7


def test_random_polygon_sides_auto():
    """
    Без параметра n_sides генерируется 3…12 вершин.
    (seed зафиксирован фикстурой → результат воспроизводим).
    """
    poly = _random_polygon()
    assert 3 <= len(poly) <= 12


# ─────────────────────────── тесты gen_random_polygon_seq ────────
def test_random_seq_count():
    """
    Последовательность случайных многоугольников отдаёт ровно `n_figs` фигур.
    """
    polys = list(gen_random_polygon_seq(n_figs=5, n_sides=4))
    assert len(polys) == 5
    assert all(len(p) == 4 for p in polys)