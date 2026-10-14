from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from calculadora import MAYOR_Y_MENOR, Calculadora

# Sin /docs ni /redoc: esas páginas cargan scripts externos que OWASP ZAP reportaría.
# El esquema /openapi.json se conserva para que ZAP conozca las rutas de la API.
app = FastAPI(title="API de la calculadora", version="1.0.0", docs_url=None, redoc_url=None)

CABECERAS_DE_SEGURIDAD = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Cache-Control": "no-store",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Referrer-Policy": "no-referrer",
}


class Peticion(BaseModel):
    # strict evita que textos como "8" se conviertan solos en números.
    model_config = ConfigDict(strict=True, allow_inf_nan=False)

    operacion: str = Field(max_length=30)
    numeros: list[float] = Field(min_length=1, max_length=100)


@app.middleware("http")
async def cabeceras_de_seguridad(request, call_next):
    respuesta = await call_next(request)
    respuesta.headers.update(CABECERAS_DE_SEGURIDAD)
    return respuesta


@app.get("/estado")
def estado():
    return {"estado": "ok"}


@app.post("/calcular")
def calcular(peticion: Peticion):
    # OBJETO: la API reutiliza la misma clase que el menú.
    objeto = Calculadora(peticion.operacion, peticion.numeros)
    try:
        respuesta = objeto.resultado()
    except (ZeroDivisionError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from None

    if objeto.operacion == MAYOR_Y_MENOR:
        respuesta = {"mayor": respuesta[0], "menor": respuesta[1]}
    return {"operacion": objeto.operacion, "numeros": peticion.numeros, "resultado": respuesta}
