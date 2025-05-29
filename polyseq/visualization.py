import itertools
from typing import Iterator

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Polygon


def visualize(polygon_seq: Iterator[tuple[tuple[float], float, ...]],
              start: int, stop: int, step: int = 1,
              ax: plt.Axes | None = None, **kwargs) -> plt.Axes:
    """
    Инструмент для визуализации указанного диапазона последовательности
    многоугольников на основе matplotlib.
    Позволяет как создать новые фигуру и оси, так и добавлять рисунок на уже существующий объект plt.Axes.

    Аргументы:
        polygon_seq: Итератор, генерирующий кортежи из вершин размера (n_sides, 2);
                     каждая вершина – кортеж координат (float, float)
        start: Индекс первой фигуры (включительно), которую нужно отобразить
        stop: Индекс последней фигуры (исключительно), которую нужно отобразить
        step: Шаг счетчика
        ax: Ось matplotlib для рисования. По умолчанию None – создается новая фигура.
        **kwargs: Необязательные параметры визуализации
                    * figsize (tuple[float, float]) — размер создаваемой фигуры, если ax is None.
                    * cmap (str | Colormap) — название или объект colormap; по умолчанию 'plasma'.
                    * alpha (float) — прозрачность патчей, по умолчанию `0.8`.
                    * fill (bool) — заполнять ли многоугольники цветом (`True`) или только контур.
                    * edgecolor (str | Tuple) — цвет линии контура (если не указан, берётся из colormap).
                    * facecolor (str | Tuple) — цвет заливки, переопределяющий colormap.

        Возвращает:
            Ось, на которой были нарисованы многоугольники
    """
    polygons = tuple(itertools.islice(polygon_seq, start, stop, step))


    def _get_color(idx: int) -> tuple[float, float, float, float] | None:
        """
        Равномерно распределяет цвета заданной цветовой карты по количеству фигур в последовательности.
        Если явно переданы edgecolor и facecolor – используем их, `_get_color()` возвращает None
        """
        if kwargs.get('edgecolor') is not None or kwargs.get('facecolor') is not None:
            return None
        else:
            cmap = plt.get_cmap(kwargs.get('cmap', 'plasma'), len(polygons))
            return cmap(idx / len(polygons))  # нормализация для равномерного распределения цветов

    # создаем новую ось, если не передана
    if ax is None:
        fig, ax = plt.subplots(figsize=kwargs.get('figsize', (7,7)))

    # рисуем
    for i, poly in enumerate(polygons):
        ax.add_patch(Polygon(poly,
                             color=_get_color(i),
                             alpha=kwargs.get('alpha', 0.8),
                             fill=kwargs.get('fill', True),
                             edgecolor=kwargs.get('edgecolor'),
                             facecolor=kwargs.get('facecolor')))

    ax.autoscale()
    ax.grid(visible=kwargs.get('grid', False))
    ax.set_aspect('equal')

    return ax