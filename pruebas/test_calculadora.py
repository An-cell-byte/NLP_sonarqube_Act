import pytest

from calculadora import Calculadora


def test_suma():
    assert Calculadora("suma", [2, 3]).resultado() == 5
    # Resultado erróneo para la lectura de errores:
    # assert Calculadora("suma", [1, 5]).resultado() == 2
    assert Calculadora("suma", [1.25, -0.5, 0.5]).resultado() == pytest.approx(1.25)


def test_resta():
    assert Calculadora("resta", [8, 3]).resultado() == 5
    assert Calculadora("resta", [-2.5, -1.25]).resultado() == pytest.approx(-1.25)


def test_multiplicacion():
    assert Calculadora("multiplicación", [2, 3, 0.5]).resultado() == pytest.approx(3)
    assert Calculadora("multiplicación", [-2, -1.5]).resultado() == pytest.approx(3)


def test_division():
    assert Calculadora("división", [9, 2]).resultado() == pytest.approx(4.5)
    assert Calculadora("división", [-7.5, 2.5]).resultado() == pytest.approx(-3)


def test_division_entre_cero():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        Calculadora("división", [9, 0]).resultado()


def test_promedio():
    assert Calculadora("promedio", [8, 9, 10]).resultado() == pytest.approx(9)
    assert Calculadora("promedio", [-1.5, 2.5, 5]).resultado() == pytest.approx(2)


def test_potencia():
    assert Calculadora("potencia", [2, 3]).resultado() == pytest.approx(8)
    assert Calculadora("potencia", [-2, 3]).resultado() == pytest.approx(-8)
    assert Calculadora("potencia", [2.5, 2]).resultado() == pytest.approx(6.25)


def test_mayor_y_menor():
    assert Calculadora("mayor y menor", [2, 3, 0.5]).resultado() == (3, 0.5)
    assert Calculadora("mayor y menor", [-2.5, -1, -3]).resultado() == (-1, -3)
