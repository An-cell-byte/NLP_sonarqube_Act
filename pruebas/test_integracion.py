<<<<<<< HEAD
import io
=======
import runpy
from pathlib import Path
>>>>>>> 5d4ad02d66fe57b6e6a8cadabb318b2067de4b63

import pytest
from fastapi.testclient import TestClient

<<<<<<< HEAD
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
=======
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
>>>>>>> 5d4ad02d66fe57b6e6a8cadabb318b2067de4b63
