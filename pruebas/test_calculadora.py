import pytest

from calculadora import (
    DIVISION,
    MAYOR_Y_MENOR,
    MULTIPLICACION,
    POTENCIA,
    PROMEDIO,
    RESTA,
    SUMA,
    Calculadora,
    formato,
)

# Resultados conocidos de cada operación.


def test_suma():
    assert Calculadora(SUMA, [2, 3]).resultado() == 5


def test_resta():
    assert Calculadora(RESTA, [3, 8]).resultado() == -5


def test_multiplicacion():
    assert Calculadora(MULTIPLICACION, [2, 3, 0.5]).resultado() == 3


def test_division():
    assert Calculadora(DIVISION, [9, 2]).resultado() == 4.5


def test_promedio():
    assert Calculadora(PROMEDIO, [8, 9, 10]).resultado() == 9


def test_potencia():
    assert Calculadora(POTENCIA, [2, 3]).resultado() == 8


def test_mayor_y_menor():
    assert Calculadora(MAYOR_Y_MENOR, [4, -7, 12, 0]).resultado() == (12, -7)


# Decimales y números negativos.


def test_suma_con_decimales():
    assert Calculadora(SUMA, [0.1, 0.2]).resultado() == pytest.approx(0.3)


def test_resta_con_negativos():
    assert Calculadora(RESTA, [-4, -10]).resultado() == 6


def test_multiplicacion_con_negativos():
    assert Calculadora(MULTIPLICACION, [-2, 4, -1.5]).resultado() == 12


def test_division_con_negativo():
    assert Calculadora(DIVISION, [-7.5, 2.5]).resultado() == -3


def test_promedio_con_decimales_y_negativos():
    assert Calculadora(PROMEDIO, [-1.5, 2.5, 5]).resultado() == pytest.approx(2)


def test_potencia_con_exponente_negativo():
    assert Calculadora(POTENCIA, [2, -2]).resultado() == 0.25


def test_potencia_con_exponente_decimal():
    assert Calculadora(POTENCIA, [16, 0.5]).resultado() == 4


def test_un_solo_numero():
    assert Calculadora(MAYOR_Y_MENOR, [5]).resultado() == (5, 5)


# Pruebas propias con datos distintos a los ejemplos.


def test_propia_promedio_de_calificaciones():
    assert Calculadora(PROMEDIO, [7.5, 9, 6.5, 10]).resultado() == pytest.approx(8.25)


def test_propia_suma_de_muchos_numeros():
    assert Calculadora(SUMA, list(range(1, 101))).resultado() == 5050


# La clase guarda los datos y acepta nombres sin acentos.


def test_guarda_operacion_y_numeros():
    objeto = Calculadora(SUMA, [1, 2])
    assert objeto.operacion == SUMA
    assert objeto.numeros == [1, 2]


@pytest.mark.parametrize(
    "nombre, numeros, esperado",
    [
        ("multiplicacion", [3, 4], 12),
        ("division", [10, 4], 2.5),
        ("mayor_y_menor", [3, 9], (9, 3)),
    ],
)
def test_nombres_sin_acentos(nombre, numeros, esperado):
    assert Calculadora(nombre, numeros).resultado() == esperado


# Errores esperados.


def test_division_entre_cero():
    with pytest.raises(ZeroDivisionError, match="No se puede dividir entre cero"):
        Calculadora(DIVISION, [5, 0]).resultado()


def test_cero_elevado_a_negativo():
    with pytest.raises(ValueError, match="potencia"):
        Calculadora(POTENCIA, [0, -1]).resultado()


def test_raiz_de_negativo():
    with pytest.raises(ValueError, match="potencia"):
        Calculadora(POTENCIA, [-8, 0.5]).resultado()


def test_potencia_demasiado_grande():
    with pytest.raises(ValueError, match="potencia"):
        Calculadora(POTENCIA, [10, 400]).resultado()


def test_resultado_demasiado_grande():
    with pytest.raises(ValueError, match="demasiado grande"):
        Calculadora(MULTIPLICACION, [1e200, 1e200]).resultado()


def test_operacion_desconocida():
    with pytest.raises(ValueError, match="Operación no válida"):
        Calculadora("raíz", [4]).resultado()


def test_lista_vacia():
    with pytest.raises(ValueError, match="al menos un número"):
        Calculadora(SUMA, []).resultado()


def test_numeros_que_no_son_lista():
    with pytest.raises(ValueError, match="al menos un número"):
        Calculadora(SUMA, 5).resultado()


@pytest.mark.parametrize("valor", ["8", None, True])
def test_valor_que_no_es_numero(valor):
    with pytest.raises(ValueError, match="Solo se aceptan números"):
        Calculadora(SUMA, [1, valor]).resultado()


def test_numero_infinito():
    with pytest.raises(ValueError, match="finitos"):
        Calculadora(SUMA, [1, float("inf")]).resultado()


@pytest.mark.parametrize("operacion", [RESTA, DIVISION, POTENCIA])
def test_operaciones_de_dos_numeros(operacion):
    with pytest.raises(ValueError, match="exactamente dos números"):
        Calculadora(operacion, [1, 2, 3]).resultado()


# Formato de los resultados que se muestran en el menú.


@pytest.mark.parametrize(
    "numero, esperado",
    [(5.0, 5), (4.5, 4.5), (0.1 + 0.2, 0.3), (-3.0, -3)],
)
def test_formato(numero, esperado):
    assert formato(numero) == esperado
