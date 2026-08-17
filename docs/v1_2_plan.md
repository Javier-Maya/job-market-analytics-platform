# v1.2 Plan — Introducing pytest

## Goal

Introduce automated testing to the project using pytest, starting
from a minimal, educational first step before testing real logic.

---

## Approved Scope

### 1. Pytest setup + trivial test

- Add `pytest` to requirements.txt
- Create `pytest.ini` with `testpaths = tests` to prevent pytest from
  scanning app/ and accidentally executing test_connection.py /
  test_s3_connection.py (which hit real Postgres/S3).
- Create tests/test_setup.py with a trivial assert-based test to
  validate the pytest harness works.

### 2. First real test (mocked)

- Create tests/test_transform_jobs.py
- Test app/processing/transform_jobs.py's mapping logic using
  unittest.mock to fake read_raw_jobs(), with no real DB connection.

Restrictions:
- Do not modify any file under app/
- Do not refactor transform_jobs.py or any other production code
- Do not touch app/db/test_connection.py or
  app/storage/test_s3_connection.py

---

## Out of Scope

- Refactoring transform_jobs.py to separate pure logic from I/O
- Testing any other module
- CI/CD integration
- Any change to Docker, Airflow, or README.md

---

## Expected Modified/Created Files

- requirements.txt (modified — add pytest)
- pytest.ini (new)
- tests/test_setup.py (new)
- tests/test_transform_jobs.py (new)

---

## Validation Checklist

- Run `pytest` and confirm tests/test_setup.py passes
- Confirm pytest does NOT collect or run anything under app/
- Run `pytest` and confirm tests/test_transform_jobs.py passes
  without any real DB/S3 connection occurring

---

## Status

Current state:
- Plan approved
- Implemented and validated
