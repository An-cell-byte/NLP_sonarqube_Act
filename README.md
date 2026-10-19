# Calculadora en Python · team4_project 

Actividad universitaria de calidad de software: una calculadora en Python con
programación orientada a objetos, pruebas automáticas y un pipeline de
integración continua en GitHub Actions. El pipeline revisa el código y la
seguridad, mide la cobertura, analiza el proyecto en SonarQube y genera un
reporte en PDF, junto con una guía para alumnos.

- Proyecto en SonarQube: `team4_project` en <https://sonarqube.lynvera.ai>
- Repositorio: <https://github.com/An-cell-byte/NLP_sonarqube_Act>

## Qué hace la calculadora

| Opción | Operación | Números | Ejemplo |
|---|---|---|---|
| 1 | Suma | 1 o más | 2, 3 y 4 → 9 |
| 2 | Resta | exactamente 2 | 3 y 8 → -5 |
| 3 | Multiplicación | 1 o más | 2, 3 y 0.5 → 3 |
| 4 | División | exactamente 2 | 9 y 2 → 4.5 |
| 5 | Promedio | 1 o más | 8, 9 y 10 → 9 |
| 6 | Potencia | exactamente 2 | 2 y 3 → 8 |
| 7 | Mayor y menor | 1 o más | 4, -2 y 8 → mayor = 8 y menor = -2 |

El menú acepta decimales con punto o coma (`2.5` o `2,5`), vuelve a pedir los
datos inválidos y muestra mensajes claros al dividir entre cero o al calcular
una potencia imposible. La misma lógica se ofrece como API HTTP con FastAPI.

## Estructura

| Ruta | Contenido |
|---|---|
| `calculadora.py` | Clase `Calculadora` y menú de consola (`main()`). |
| `api.py` | API FastAPI: `GET /estado` y `POST /calcular`. |
| `pruebas/` | Pruebas unitarias, de integración y del reporte (pytest). |
| `herramientas/` | Descarga de resultados de SonarQube y generación de los PDF. |
| `GUIA_ALUMNOS.md` | Texto de la guía para alumnos. |
| `material/GUIA_ALUMNOS.pdf` | Guía en PDF, generada a partir del Markdown. |
| `.github/workflows/ci.yml` | Pipeline principal **Calidad y seguridad**. |
| `.github/workflows/build.yml` | Análisis de SonarQube de la primera práctica; solo se ejecuta manualmente. |
| `pyproject.toml` | Configuración de pytest, coverage y ruff. |
| `sonar-project.properties` | Configuración del análisis de SonarQube. |
| `requirements.txt` | Dependencias con versiones fijas. |

## Requisitos e instalación

Python 3.12 o posterior.

```sh
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En Windows instala también `tzdata` (`python -m pip install tzdata`). El reporte
PDF usa la zona horaria `America/Monterrey`, y Windows no incluye esa base de
datos. Sin ella falla localmente `test_crear_reportes`. En GitHub Actions no hace
falta, porque los runners usan Linux.

## Uso

Menú de consola:

```sh
python calculadora.py
```

API local:

```sh
uvicorn api:aplicacion --reload
```

Ejemplo de petición:

```sh
curl -X POST http://127.0.0.1:8000/calcular \
  -H "Content-Type: application/json" \
  -d '{"operacion": "promedio", "numeros": [8, 9, 10]}'
# {"resultado":9.0}
```

| Respuesta | Cuándo |
|---|---|
| `200` | Cálculo correcto: `{"resultado": ...}` |
| `400` | División entre cero o potencia que no se puede calcular. |
| `422` | Operación desconocida, lista vacía o cantidad de números incorrecta. |

Las operaciones válidas son `suma`, `resta`, `multiplicación`, `división`,
`promedio`, `potencia` y `mayor y menor`.

## Pruebas y cobertura

```sh
python -m pytest                                  # todas las pruebas
python -m pytest --cov --cov-report=term-missing  # con cobertura y líneas faltantes
```

| Archivo | Qué comprueba |
|---|---|
| `pruebas/test_calculadora.py` | Cada operación de la clase y la división entre cero. |
| `pruebas/test_integracion.py` | El menú completo y la API. El menú se ejecuta en el mismo proceso de pytest, con `monkeypatch` y `capsys`, para que coverage lo mida. |
| `pruebas/test_reporte.py` | Los PDF, el JSON y el Markdown, y la consulta a SonarQube con respuestas simuladas, sin red ni token. |

La cobertura mínima es de **90 %** de líneas y ramas, y abarca `calculadora.py`,
`api.py` y `herramientas/`. Revisión de estilo:

```sh
ruff check .
ruff format --check .
```

## Pipeline de CI

`ci.yml` se ejecuta en cada pull request, en cada push a `main` y manualmente
desde la pestaña **Actions**.

| Job | Qué hace |
|---|---|
| `revision` | ruff: errores y formato. |
| `unitarias` | Pruebas de la calculadora y del reporte. |
| `integracion` | Pruebas del menú y de la API. |
| `cobertura` | Todas las pruebas con cobertura; genera `coverage.xml`. |
| `secretos` | Gitleaks busca credenciales en el historial. |
| `seguridad` | Bandit busca patrones inseguros en el código. |
| `dependencias` | pip-audit busca vulnerabilidades conocidas. |
| `obsoletas` | Lista de dependencias con versiones nuevas (informativo). |
| `zap` | OWASP ZAP prueba la API en ejecución dentro del runner. |
| `sonarqube` | Análisis en SonarQube con la cobertura (solo en `main`). |
| `reporte` | Descarga el análisis, genera los PDF y evalúa el Quality Gate (solo en `main`). |
| `resumen` | Tabla final con el resultado de todos los jobs. |

En los pull requests, `sonarqube` y `reporte` aparecen omitidos. Es lo esperado:
el análisis se reserva para `main`.

### Configuración necesaria

Guarda el secreto `SONAR_TOKEN` en **Settings → Secrets and variables →
Actions**. Debe ser un User Token con permisos **Browse** y **Execute Analysis**
sobre `team4_project`. La URL del servidor ya está definida en `ci.yml`.

### Flujo de trabajo 

1. Crea una rama, haz tus cambios y ejecuta `python -m pytest`.
2. Haz push de la rama y abre un pull request hacia `main`.
3. Cuando los checks estén en verde, integra el PR. El push resultante a `main`
   ejecuta SonarQube y genera los reportes.

## Reportes

Al terminar una ejecución en `main`, en **Actions → ejecución → Artifacts**:

| Artifact | Contenido |
|---|---|
| `sonarqube-report-pdf-json-md` | Reporte de calidad: Quality Gate, cobertura, issues y commit analizado (`sonarqube.pdf`, `.json` y `.md`). |
| `guia-para-alumnos-pdf` | Guía para alumnos regenerada. |
| `cobertura` | `coverage.xml` y `reports/junit.xml`. |
| `secret-scan`, `static-security`, `dependency-audit`, `outdated-dependencies`, `owasp-zap` | Resultados de cada herramienta de seguridad. |

Para regenerar la guía localmente después de editar `GUIA_ALUMNOS.md`:

```sh
python -m herramientas.guia_pdf
```

El reporte de SonarQube (`python -m herramientas.reporte_sonarqube`) está pensado
para ejecutarse dentro de GitHub Actions. Necesita el archivo que deja el
escáner y las variables `SONAR_TOKEN` y `GITHUB_SHA`.
