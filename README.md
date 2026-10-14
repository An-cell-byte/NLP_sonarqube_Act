# Calculadora con pruebas automáticas, API y SonarQube

Calculadora orientada a objetos (clase `Calculadora`) con menú en consola, API con FastAPI y un
workflow de GitHub Actions que comprueba funcionamiento, cobertura y seguridad.

## Estructura

| Archivo | Contenido |
| --- | --- |
| `calculadora.py` | Clase `Calculadora` (una operación por método, `resultado()` elige el método) y menú. |
| `api.py` | API: `GET /estado` y `POST /calcular`, reutiliza `Calculadora`. |
| `pruebas/test_calculadora.py` | Pruebas unitarias de cada operación, decimales, negativos y errores. |
| `pruebas/test_integracion.py` | Recorridos del menú y de la API. |
| `pyproject.toml` | Configuración de pytest, cobertura (mínimo 90 %), Ruff y Bandit. |
| `sonar-project.properties` | Clave `team4_project`, archivos analizados y ruta de `coverage.xml`. |
| `.github/workflows/ci.yml` | Workflow de integración continua. |

## Uso local

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt

python calculadora.py
python -m uvicorn api:app --reload
```

Ejemplo con la API:

```bash
curl -X POST http://localhost:8000/calcular -H "Content-Type: application/json" \
     -d '{"operacion": "promedio", "numeros": [8, 9, 10]}'
# {"operacion":"promedio","numeros":[8.0,9.0,10.0],"resultado":9.0}
```

Operaciones: `suma`, `resta`, `multiplicación` (o `multiplicacion`), `división` (o `division`),
`promedio`, `potencia` y `mayor y menor` (o `mayor_y_menor`). Un error de cálculo devuelve 400 y
datos mal formados devuelven 422.

## Revisiones antes de guardar cambios

```bat
python -m ruff check .
python -m ruff format --check .
python -m pytest --cov --cov-report=term-missing --cov-report=xml
```

## Workflow de GitHub Actions

Se ejecuta en `push` a `main`, en cada pull request y de forma manual.

| Job | Responsabilidad | Espera a |
| --- | --- | --- |
| revision | Ruff: código y formato. | - |
| unitarias | Pruebas unitarias. | - |
| integracion | Pruebas del menú y la API. | unitarias |
| cobertura | Todas las pruebas y `coverage.xml` (mínimo 90 %). | unitarias, integracion |
| secretos | Gitleaks sobre todo el historial. | - |
| seguridad | Bandit sobre el código Python. | - |
| dependencias | pip-audit sobre `requirements.txt`. | - |
| obsoletas | Lista bibliotecas con versiones nuevas (informativo). | - |
| zap | OWASP ZAP sobre la API levantada temporalmente. | integracion, secretos, seguridad, dependencias |
| sonarqube | Análisis, importación de cobertura y Quality Gate (solo `main`). | cobertura, revision, secretos, seguridad, dependencias |
| resumen | Estado de todos los controles (`if: always()`). | todos |

En los pull requests `sonarqube` aparece omitido; es lo esperado.

## SonarQube

- Servidor: https://sonarqube.lynvera.ai, proyecto `team4_project`.
- El secreto `SONAR_TOKEN` (User Token con permisos Browse y Execute Analysis) se guarda en
  *Settings → Secrets and variables → Actions*. Nunca se escribe en los archivos.
