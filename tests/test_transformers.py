import math
import pytest

from polyseq.transformers import tr_translate, tr_rotate, tr_symmetry, tr_homothety

# Тестовый многоугольник (квадрат)
SQUARE = ((0,0), (1,0), (1,1), (0,1))

# ----------------- tr_translate -----------------
def test_tr_translate_basic():
    # сдвигаем квадрат на (1, 2)
    translated = tr_translate(SQUARE, 1, 2)
    expected = ((1,2), (2,2), (2,3), (1,3))
    for v1, v2 in zip(translated, expected):
        assert math.isclose(v1[0], v2[0])
        assert math.isclose(v1[1], v2[1])

def test_tr_translate_type_error():
    # dx/dy должны быть числами
    with pytest.raises(TypeError):
        tr_translate(SQUARE, 'a', 1)
    with pytest.raises(TypeError):
        tr_translate(SQUARE, 1, None)


# ----------------- tr_rotate -----------------
def test_tr_rotate_90_degrees():
    # Поворот квадрата на 90 градусов против часовой стрелки
    rotated = tr_rotate(SQUARE, 90)
    expected = ((0,0), (0,1), (-1,1), (-1,0))
    for v1, v2 in zip(rotated, expected):
        assert math.isclose(v1[0], v2[0], abs_tol=1e-9)
        assert math.isclose(v1[1], v2[1], abs_tol=1e-9)

def test_tr_rotate_type_error():
    with pytest.raises(TypeError):
        tr_rotate(SQUARE, "ninety")


# ----------------- tr_symmetry -----------------
@pytest.mark.parametrize("axis, expected", [
    ('x', ((0,0), (1,0), (1,-1), (0,-1))),
    (0,   ((0,0), (1,0), (1,-1), (0,-1))),
    ('y', ((0,0), (-1,0), (-1,1), (0,1))),
    (1,   ((0,0), (-1,0), (-1,1), (0,1))),
])
def test_tr_symmetry_valid_axes(axis, expected):
    reflected = tr_symmetry(SQUARE, axis)
    for v1, v2 in zip(reflected, expected):
        assert math.isclose(v1[0], v2[0], abs_tol=1e-9)
        assert math.isclose(v1[1], v2[1], abs_tol=1e-9)

def test_tr_symmetry_invalid_axis():
    with pytest.raises(ValueError):
        tr_symmetry(SQUARE, 'z')
    with pytest.raises(ValueError):
        tr_symmetry(SQUARE, 2)


# ----------------- tr_homothety -----------------
def test_tr_homothety_scale_up():
    center = (0,0)
    k = 2
    scaled = tr_homothety(SQUARE, center, k)
    expected = ((0,0), (2,0), (2,2), (0,2))
    for v1, v2 in zip(scaled, expected):
        assert math.isclose(v1[0], v2[0], abs_tol=1e-9)
        assert math.isclose(v1[1], v2[1], abs_tol=1e-9)

def test_tr_homothety_scale_down():
    center = (0,0)
    k = 0.5
    scaled = tr_homothety(SQUARE, center, k)
    expected = ((0,0), (0.5,0), (0.5,0.5), (0,0.5))
    for v1, v2 in zip(scaled, expected):
        assert math.isclose(v1[0], v2[0], abs_tol=1e-9)
        assert math.isclose(v1[1], v2[1], abs_tol=1e-9)

def test_tr_homothety_center_not_tuple():
    with pytest.raises(TypeError):
        tr_homothety(SQUARE, ('a', 0), 2)

def test_tr_homothety_k_zero_value_error():
    with pytest.raises(ValueError):
        tr_homothety(SQUARE, (0,0), 0)

def test_tr_homothety_k_not_number():
    with pytest.raises(TypeError):
        tr_homothety(SQUARE, (0,0), 'big')

def test_tr_homothety_negative_k():
    center = (0,0)
    k = -1
    scaled = tr_homothety(SQUARE, center, k)
    expected = tuple((-x, -y) for x, y in SQUARE)
    for v1, v2 in zip(scaled, expected):
        assert math.isclose(v1[0], v2[0], abs_tol=1e-9)
        assert math.isclose(v1[1], v2[1], abs_tol=1e-9)
