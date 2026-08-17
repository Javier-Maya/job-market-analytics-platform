# v1.1 Plan — Minimal Logging + DB Health Check

## Goal

Improve operational visibility and API health validation
without changing the current project architecture.

---

## Approved Scope

### 1. Structured logging

Add minimal structured logging only in:

app/pipeline/run_pipeline.py

Goals:
- Track pipeline start/end
- Track stage execution
- Improve debugging visibility

Restrictions:
- Do not create shared logging modules
- Do not add external logging packages
- Do not modify loader modules

---

### 2. PostgreSQL-backed health check

Improve:

app/api/main.py

Current issue:
- /health only verifies API availability
- It does not validate database connectivity

Goal:
- Verify PostgreSQL connectivity through a lightweight query

Restrictions:
- Do not modify connection.py unless strictly necessary

---

## Out of Scope

The following files must NOT be modified:

- fetch_jobs.py
- load_raw_jobs_from_s3.py
- load_clean_jobs.py
- load_skills.py
- Airflow DAGs
- Docker configuration
- README.md

No:
- refactors
- architecture redesign
- dependency changes

---

## Expected Modified Files

- app/pipeline/run_pipeline.py
- app/api/main.py

---

## Validation Checklist

### Logging
- Run pipeline manually
- Verify logs show stage lifecycle clearly

### Health Check
- Verify /health returns healthy when PostgreSQL is running
- Stop PostgreSQL and verify unhealthy response

---

## Status

Current state:
- Plan approved
- Pending implementation