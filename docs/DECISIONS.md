# Decisiones técnicas

## Health check de PostgreSQL: SELECT 1 propio vs. librería de healthcheck

### Contexto
`/health` en `app/api/main.py` solo confirmaba que la API respondía, no que PostgreSQL estuviera disponible. El plan v1.1 restringía explícitamente "no agregar dependencias".

### Decisión
Implementar el chequeo con una query mínima (`SELECT 1`) usando la conexión ya existente (`get_connection`), envuelta en `try/except`, devolviendo HTTP 503 si falla — sin agregar ninguna librería externa de healthcheck (ej. `fastapi-health`).

### Razón
El chequeo es trivial (una sola query), no justifica el costo de una dependencia nueva (mantenimiento, superficie de auditoría, rebuild de imagen Docker). Además, el proyecto es un portafolio de Data Engineering: usar SQL crudo demuestra mejor el fundamento técnico que instalar un plugin para algo tan simple.

### Trade-offs
Si en el futuro se necesitan checks más sofisticados (múltiples dependencias, timeouts configurables, health check agregado), una librería dedicada podría justificarse. Hoy no.

---

## Test de transform_jobs: mock de read_raw_jobs vs. refactor para separar lógica pura

### Contexto
`transform_jobs()` mezcla lógica de transformación con I/O directo a PostgreSQL (llama a `read_raw_jobs()` internamente), lo que dificulta testearlo sin una base de datos real.

### Decisión
Testear usando `unittest.mock.patch` para reemplazar `read_raw_jobs` en el namespace de `transform_jobs.py`, en vez de refactorizar el código de producción para separar la lógica pura del I/O.

### Razón
El plan v1.2 excluye explícitamente refactors de código de producción. Mockear enseña una habilidad transferible (aislar dependencias externas en tests) sin tocar `app/`.

### Trade-offs
El test queda acoplado a la forma exacta en que `transform_jobs.py` importa `read_raw_jobs` (`from ... import read_raw_jobs`) — si cambia el import, el patch se rompe. Un refactor hacia una función pura sería más robusto a futuro, pero es una decisión pendiente, no tomada.

---

## Aislar pytest con testpaths=tests vs. modificar los scripts test_* existentes

### Contexto
Ya existían `app/db/test_connection.py` y `app/storage/test_s3_connection.py`, dos scripts de diagnóstico manual cuyos nombres coinciden con la convención de descubrimiento de pytest (`test_*.py`, funciones `test_*`). Si pytest los recolectara, ejecutaría conexiones reales a PostgreSQL y S3 por accidente.

### Decisión
Configurar `pytest.ini` con `testpaths = tests`, restringiendo el descubrimiento de pytest a una carpeta `tests/` dedicada, sin tocar ni renombrar los scripts existentes.

### Razón
Resuelve el riesgo real sin modificar código de producción/diagnóstico ya funcional, cumpliendo la restricción del plan v1.2 de no tocar `app/`.

### Trade-offs
Si en el futuro se agregan más scripts de diagnóstico fuera de `tests/` con nombres `test_*`, seguirán siendo invisibles para pytest — la protección depende de la ubicación del archivo, no de una convención de nombre.
