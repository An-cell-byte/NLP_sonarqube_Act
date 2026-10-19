import io

import pytest
from fastapi.testclient import TestClient

from api import aplicacion
from calculadora import main

cliente = TestClient(aplicacion)


@pytest.fixture
def ejecutar_menu(monkeypatch, capsys):
    """Ejecuta main() en el mismo proceso de pytest para que coverage lo mida."""

    def _ejecutar(respuestas):
        monkeypatch.setattr("sys.stdin", io.StringIO(respuestas))
        main()
        return capsys.readouterr().out

    return _ejecutar


def test_menu_muestra_el_calculo_correcto(ejecutar_menu):
    casos = [
        ("1\n2\n2\n3", "Resultado: 5"),
        ("1\n3\n1.25\n-0.5\n0.5", "Resultado: 1.25"),
        ("2\n8\n3", "Resultado: 5"),
        ("2\n-2.5\n-1.25", "Resultado: -1.25"),
        ("3\n3\n2\n3\n0.5", "Resultado: 3"),
        ("3\n2\n-2\n-1.5", "Resultado: 3"),
        ("4\n9\n2", "Resultado: 4.5"),
        ("4\n-7.5\n2.5", "Resultado: -3"),
        ("4\n9\n0", "Error: no se puede dividir entre cero."),
        ("5\n3\n8\n9\n10", "Resultado: 9"),
        ("5\n3\n-1.5\n2.5\n5", "Resultado: 2"),
        ("6\n2\n3", "Resultado: 8"),
        ("6\n-2\n3", "Resultado: -8"),
        ("6\n2.5\n2", "Resultado: 6.25"),
        ("7\n3\n2\n3\n0.5", "Resultado: mayor = 3 y menor = 0.5"),
        ("7\n3\n-2.5\n-1\n-3", "Resultado: mayor = -1 y menor = -3"),
    ]
    respuestas = "\n".join(entrada for entrada, _ in casos) + "\n0\n"
    salida = ejecutar_menu(respuestas)

    for _, resultado_esperado in casos:
        assert resultado_esperado in salida
    assert "Programa terminado." in salida


def test_menu_permite_continuar_con_otra_operacion_y_salir(ejecutar_menu):
    salida = ejecutar_menu("1\n2\n2\n3\n2\n8\n3\n0\n")

    assert salida.count("===== CALCULADORA =====") == 3
    assert salida.count("Resultado: 5") == 2
    assert "Programa terminado." in salida


def test_entrada_incorrecta_no_cierra_el_programa(ejecutar_menu):
    salida = ejecutar_menu("opción incorrecta\n1\n2\n2\n3\n0\n")

    assert "Opción no válida." in salida
    assert "Resultado: 5" in salida
    assert "Programa terminado." in salida


def test_numero_no_valido_se_vuelve_a_pedir(ejecutar_menu):
    salida = ejecutar_menu("2\nabc\n8\n3\n0\n")

    assert "Valor no válido." in salida
    assert "Resultado: 5" in salida


def test_numero_con_coma_decimal(ejecutar_menu):
    salida = ejecutar_menu("4\n9\n2,5\n0\n")

    assert "Resultado: 3.6" in salida


def test_cantidad_no_valida_se_vuelve_a_pedir(ejecutar_menu):
    salida = ejecutar_menu("1\n0\ndos\n2\n2\n3\n0\n")

    assert salida.count("Cantidad no válida.") == 2
    assert "Resultado: 5" in salida


def test_potencia_con_valores_no_calculables(ejecutar_menu):
    salida = ejecutar_menu("6\n0\n-1\n6\n10\n1000\n0\n")

    assert salida.count("Error: no se puede calcular con esos valores.") == 2


def test_api_recibe_operacion_y_devuelve_resultado():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "suma", "numeros": [2, 3]},
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {"resultado": 5}


def test_api_devuelve_error_comprensible_al_dividir_entre_cero():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "división", "numeros": [9, 0]},
    )

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "No se puede dividir entre cero."}


def test_api_estado_responde_correcto():
    respuesta = cliente.get("/estado")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "correcto"}


def test_api_rechaza_operacion_no_valida():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "raíz", "numeros": [9]},
    )

    assert respuesta.status_code == 422
    assert respuesta.json() == {"error": "Envía una operación y sus números."}


def test_api_exige_dos_numeros_en_operaciones_binarias():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "resta", "numeros": [8, 3, 1]},
    )

    assert respuesta.status_code == 422
    assert respuesta.json() == {"detail": "La operación resta requiere exactamente dos números."}


def test_api_devuelve_error_con_potencia_no_calculable():
    for numeros in ([0, -1], [10, 1000]):
        respuesta = cliente.post(
            "/calcular",
            json={"operacion": "potencia", "numeros": numeros},
        )

        assert respuesta.status_code == 400
        assert "math" in respuesta.json()["detail"]
