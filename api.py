from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from calculadora import Calculadora

aplicacion = FastAPI(title="Calculadora", docs_url=None, redoc_url=None)

Operacion = Literal[
    "suma",
    "resta",
    "multiplicación",
    "división",
    "promedio",
    "potencia",
    "mayor y menor",
]


class SolicitudCalculo(BaseModel):
    operacion: Operacion
    numeros: list[float] = Field(min_length=1, max_length=1000)


@aplicacion.exception_handler(RequestValidationError)
async def entrada_invalida(peticion, error):
    return JSONResponse(status_code=422, content={"error": "Envía una operación y sus números."})


@aplicacion.middleware("http")
async def agregar_cabeceras(peticion, siguiente):
    respuesta = await siguiente(peticion)
    respuesta.headers.update(
        {
            "Content-Security-Policy": (
                "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
            ),
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Cross-Origin-Resource-Policy": "same-origin",
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
        }
    )
    return respuesta


@aplicacion.get("/estado")
def estado():
    return {"estado": "correcto"}


@aplicacion.post("/calcular")
def calcular(datos: SolicitudCalculo):
    numeros = datos.numeros
    operacion = datos.operacion
    if operacion in {"resta", "división", "potencia"} and len(numeros) != 2:
        raise HTTPException(
            status_code=422,
            detail=f"La operación {operacion} requiere exactamente dos números.",
        )

    try:
        calculadora = Calculadora(operacion, numeros)
        resultado = calculadora.resultado()
        return {"resultado": resultado}
    except ZeroDivisionError as error:
        raise HTTPException(
            status_code=400,
            detail="No se puede dividir entre cero.",
        ) from error
    except (ValueError, OverflowError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
