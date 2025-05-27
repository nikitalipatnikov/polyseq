import math
import itertools
import pytest
import matplotlib
matplotlib.use("Agg")  # без GUI
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from polyseq.visualization import visualize


# Простые полигоны для теста
SQUARE = ((0,0), (1,0), (1,1), (0,1))
TRIANGLE = ((0,0), (1,0), (0.5,0.866))


def polygon_seq():
    """Генератор из двух фигур."""
    yield SQUARE
    yield TRIANGLE


def test_visualize_creates_new_axes():
    ax = visualize(polygon_seq(), 0, 2)
    assert isinstance(ax, plt.Axes)
    # Проверяем, что на оси два патча
    assert len(ax.patches) == 2
    # Патчи - объекты Polygon
    assert all(isinstance(p, Polygon) for p in ax.patches)

def test_visualize_with_existing_axes():
    fig, ax = plt.subplots()
    ax_result = visualize(polygon_seq(), 0, 2, ax=ax, alpha=0.5)
    # Проверяем, что функция вернула тот же объект оси
    assert ax is ax_result
    # Проверяем количество патчей
    assert len(ax.patches) == 2

def test_visualize_step_and_slice():
    # Возьмем только 1 фигуру с шагом 2 - должен быть SQUARE
    ax = visualize(polygon_seq(), 0, 2, step=2)
    assert len(ax.patches) == 1
    # Проверяем координаты первой вершины патча совпадают с SQUARE
    patch = ax.patches[0]
    assert math.isclose(patch.get_xy()[0][0], SQUARE[0][0])
    assert math.isclose(patch.get_xy()[0][1], SQUARE[0][1])

def test_visualize_with_kwargs():
    # Проверяем передачу alpha и fill
    ax = visualize(polygon_seq(), 0, 2, alpha=0.3, fill=False)
    for patch in ax.patches:
        assert math.isclose(patch.get_alpha(), 0.3)
        assert patch.get_fill() is False

def test_visualize_limits_and_aspect():
    ax = visualize(polygon_seq(), 0, 2)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    # Проверяем, что пределы больше, чем минимальные координаты на ±1
    xs = [v[0] for poly in [SQUARE, TRIANGLE] for v in poly]
    ys = [v[1] for poly in [SQUARE, TRIANGLE] for v in poly]
    assert xlim[0] < min(xs)
    assert xlim[1] > max(xs)
    assert ylim[0] < min(ys)
    assert ylim[1] > max(ys)
    assert ax.get_aspect() == 1.0
