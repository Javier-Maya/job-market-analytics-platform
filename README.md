# Job Market Analytics Platform

Plataforma de Data Engineering desarrollada para ingerir, procesar, modelar y exponer información de ofertas laborales obtenidas desde una API pública.

El proyecto implementa un pipeline end-to-end que captura datos desde Remotive Jobs, almacena información raw en Amazon S3, transforma y modela los datos en PostgreSQL y finalmente expone información analítica mediante una API REST construida con FastAPI.

La ejecución completa del pipeline es orquestada mediante Apache Airflow y Docker.

---

## Objetivo

El objetivo de este proyecto es construir una plataforma de datos completa capaz de:

- Ingerir información desde una API externa.
- Mantener almacenamiento raw siguiendo buenas prácticas de Data Engineering.
- Procesar y transformar datos para análisis posterior.
- Aplicar modelado relacional y normalización.
- Exponer información mediante una API REST.
- Automatizar la ejecución del pipeline mediante Airflow.

---

## Arquitectura

```text
Remotive Jobs API
        │
        ▼
 Amazon S3
 (Raw JSON)
        │
        ▼
 PostgreSQL
 (raw_jobs)
        │
        ▼
 Transformación
        │
        ▼
 clean_jobs
        │
        ├───────────────┐
        ▼               ▼
     skills       job_skills
        │
        ▼
      FastAPI
        │
        ▼
     Swagger UI
```

---

## Fuente de Datos

Las ofertas laborales son obtenidas desde la API pública de Remotive:

https://remotive.com

La información incluye:

- Título del cargo
- Empresa
- Ubicación
- Tipo de empleo
- Fecha de publicación
- Skills y tags asociados
- Descripción del empleo

---

## Stack Tecnológico

| Categoría | Tecnologías |
|------------|------------|
| Lenguaje | Python |
| Base de Datos | PostgreSQL |
| API | FastAPI, Uvicorn |
| Orquestación | Apache Airflow |
| Cloud Storage | Amazon S3 |
| Contenedores | Docker, Docker Compose |
| Librerías | boto3, psycopg2 |
| Modelado de Datos | SQL, Normalización, Relaciones many-to-many |

---

## Flujo del Pipeline

### 1. Ingesta

Obtención de ofertas laborales desde la API pública Remotive.

### 2. Raw Storage

Los datos originales son almacenados en formato JSON dentro de Amazon S3 para preservar la información sin transformar.

### 3. Carga a PostgreSQL

Los datos raw son cargados a la tabla:

- `raw_jobs`

### 4. Transformación

Los datos son limpiados y estructurados en campos relevantes:

- `source_job_id`
- `title`
- `company`
- `location`
- `job_type`
- `publication_date`

Generando la tabla:

- `clean_jobs`

### 5. Modelado

Extracción y normalización de habilidades mediante:

- `skills`
- `job_skills`

Implementando relaciones many-to-many para evitar duplicidad y facilitar consultas analíticas.

### 6. Exposición

Los datos procesados son publicados mediante FastAPI para consumo externo.

---

## Endpoints Disponibles

### Health Check

```http
GET /health
```

### Listado de empleos

```http
GET /jobs
```

### Empleo por ID

```http
GET /jobs/{job_id}
```

### Skills disponibles

```http
GET /skills
```

### Skills más demandadas

```http
GET /skills/top
```

---

## Orquestación con Airflow

La ejecución completa del pipeline es administrada mediante Apache Airflow utilizando un `DockerOperator`.

El DAG ejecuta el worker principal:

```bash
python -m app.pipeline.run_pipeline
```

Pipeline ejecutado:

1. Ingesta desde Remotive
2. Almacenamiento raw en Amazon S3
3. Carga hacia PostgreSQL (`raw_jobs`)
4. Transformación hacia `clean_jobs`
5. Generación de `skills`
6. Generación de relaciones `job_skills`

---

## Resultados

La plataforma permite:

- Consultar ofertas laborales procesadas mediante API REST.
- Analizar las habilidades más demandadas del mercado.
- Ejecutar pipelines de forma automatizada mediante Airflow.
- Mantener almacenamiento raw y transformado siguiendo buenas prácticas de Data Engineering.
- Aplicar modelado relacional para facilitar análisis posteriores.

---

## Ejecución Local

### 1. Clonar el repositorio

```bash
git clone <repository_url>
cd job-market-analytics-platform
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Completar los valores correspondientes para:

- PostgreSQL
- AWS S3
- Credenciales AWS

### 3. Levantar la infraestructura

```bash
docker compose up -d --build
```

### 4. Acceder a los servicios

#### FastAPI Swagger

```text
http://localhost:8000/docs
```

#### Health Check

```text
http://localhost:8000/health
```

#### Apache Airflow

```text
http://localhost:8080
```

---

## Estructura del Proyecto

```text
airflow/
├── dags/
├── logs/
└── plugins/

app/
├── api/
├── db/
├── ingestion/
├── pipeline/
├── processing/
├── storage/
└── worker/

data/
└── raw/

docker-compose.yml
Dockerfile
requirements.txt
README.md
.env.example
```

---

## Próximas Mejoras

- Implementación de pruebas automatizadas (pytest)
- Integración continua mediante GitHub Actions
- Despliegue en AWS
- Monitoreo y observabilidad
- Dashboard analítico
- Data Warehouse para análisis históricos

---

## Autor

**Javier Maya Navarrete**

Data Engineer | SQL · Python · ETL | AWS Certified | Data Integration & Automation

LinkedIn: https://www.linkedin.com/in/javier-maya-navarrete/

GitHub: https://github.com/Javier-Maya/