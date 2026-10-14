import runpy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import app
from calculadora import MENSAJE_SALIDA, main

cliente = TestClient(app)
RUTA_CALCULAR = "/calcular"


def calcular(operacion, numeros):
    """Envía una operación a la API y devuelve la respuesta."""
    return cliente.post(RUTA_CALCULAR, json={"operacion": operacion, "numeros": numeros})


def simular_entradas(monkeypatch, respuestas):
    """Hace que input() devuelva las respuestas en orden, como si las escribiera el usuario."""
    respuestas = iter(respuestas)

    def entrada_falsa(_mensaje=""):
        try:
            return next(respuestas)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr("builtins.input", entrada_falsa)


# Recorridos por el menú.


def test_menu_calcula_suma(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["1", "2", "2", "3", "0"])
    main()
    salida = capsys.readouterr().out
    assert "Resultado: 5" in salida
    assert MENSAJE_SALIDA in salida


def test_menu_calcula_promedio_con_coma_decimal(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["5", "2", "7,5", "8,5", "0"])
    main()
    assert "Resultado: 8" in capsys.readouterr().out


def test_menu_muestra_orden_de_la_resta(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["2", "3", "8", "0"])
    main()
    salida = capsys.readouterr().out
    assert "Orden: primero menos segundo" in salida
    assert "Resultado: -5" in salida


def test_menu_mayor_y_menor(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["7", "3", "4", "-2", "9", "0"])
    main()
    assert "Resultado: mayor = 9 y menor = -2" in capsys.readouterr().out


def test_menu_permite_continuar_y_salir(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["3", "2", "4", "5", "6", "2", "3", "0"])
    main()
    salida = capsys.readouterr().out
    assert "Resultado: 20" in salida
    assert "Resultado: 8" in salida
    assert salida.count("===== CALCULADORA =====") == 3
    assert salida.strip().endswith(MENSAJE_SALIDA)


def test_menu_sale_inmediatamente(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["0"])
    main()
    salida = capsys.readouterr().out
    assert "Resultado" not in salida
    assert MENSAJE_SALIDA in salida


# Entradas incorrectas: el programa avisa y continúa.


def test_menu_opcion_no_valida(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["9", "abc", "1", "1", "4", "0"])
    main()
    salida = capsys.readouterr().out
    assert salida.count("Opción no válida") == 2
    assert "Resultado: 4" in salida


def test_menu_numero_no_valido(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["4", "diez", "inf", "10", "4", "0"])
    main()
    salida = capsys.readouterr().out
    assert "Valor no válido. Escribe un número" in salida
    assert "Valor no válido. Escribe un número finito." in salida
    assert "Resultado: 2.5" in salida


def test_menu_cantidad_no_valida(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["1", "0", "-3", "dos", "2", "1", "1", "0"])
    main()
    salida = capsys.readouterr().out
    assert salida.count("Cantidad no válida") == 3
    assert "Resultado: 2" in salida


def test_menu_division_entre_cero(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["4", "5", "0", "1", "1", "1", "0"])
    main()
    salida = capsys.readouterr().out
    assert "Error: No se puede dividir entre cero." in salida
    assert "Resultado: 1" in salida


def test_menu_potencia_no_calculable(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["6", "0", "-1", "0"])
    main()
    assert "Error: No se puede calcular la potencia" in capsys.readouterr().out


def test_menu_termina_si_se_cierra_la_entrada(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["1"])
    main()
    assert MENSAJE_SALIDA in capsys.readouterr().out


def test_ejecutar_como_programa(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["0"])
    ruta = Path(__file__).resolve().parent.parent / "calculadora.py"
    runpy.run_path(str(ruta), run_name="__main__")
    assert MENSAJE_SALIDA in capsys.readouterr().out


# API.


def test_api_estado():
    respuesta = cliente.get("/estado")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_api_promedio():
    respuesta = calcular("promedio", [8, 9, 10])
    assert respuesta.status_code == 200
    assert respuesta.json()["resultado"] == 9


@pytest.mark.parametrize(
    "operacion, numeros, esperado",
    [
        ("suma", [2, 3], 5),
        ("resta", [3, 8], -5),
        ("multiplicacion", [2, 3, 0.5], 3),
        ("división", [9, 2], 4.5),
        ("potencia", [2, 3], 8),
    ],
)
def test_api_operaciones(operacion, numeros, esperado):
    respuesta = calcular(operacion, numeros)
    assert respuesta.status_code == 200
    assert respuesta.json()["resultado"] == esperado


def test_api_mayor_y_menor():
    respuesta = calcular("mayor y menor", [3, -1, 7])
    assert respuesta.status_code == 200
    assert respuesta.json()["resultado"] == {"mayor": 7, "menor": -1}


def test_api_division_entre_cero():
    respuesta = calcular("división", [1, 0])
    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "No se puede dividir entre cero."


def test_api_operacion_desconocida():
    respuesta = calcular("raiz", [4])
    assert respuesta.status_code == 400
    assert "Operación no válida" in respuesta.json()["detail"]


@pytest.mark.parametrize(
    "datos",
    [
        {"operacion": "suma"},
        {"operacion": "suma", "numeros": []},
        {"operacion": "suma", "numeros": ["8", "9"]},
        {"operacion": "suma", "numeros": "8"},
        {"operacion": 5, "numeros": [1]},
        {"operacion": "suma", "numeros": list(range(101))},
    ],
)
def test_api_rechaza_datos_incorrectos(datos):
    assert cliente.post(RUTA_CALCULAR, json=datos).status_code == 422


def test_api_rechaza_json_mal_formado():
    respuesta = cliente.post(
        RUTA_CALCULAR, content="{no es json", headers={"Content-Type": "application/json"}
    )
    assert respuesta.status_code == 422


def test_api_cabeceras_de_seguridad():
    respuesta = cliente.get("/estado")
    assert respuesta.headers["X-Content-Type-Options"] == "nosniff"
    assert respuesta.headers["X-Frame-Options"] == "DENY"
