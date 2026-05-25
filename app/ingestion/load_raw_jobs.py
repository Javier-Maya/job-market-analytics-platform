import json
from pathlib import Path

from app.db.connection import get_connection


def get_latest_raw_file() -> Path:
    raw_dir = Path("data/raw")
    files = sorted(raw_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError("No se encontraron archivos JSON en data/raw")
    return files[-1]


def load_raw_jobs():
    conn = get_connection()

    cursor = conn.cursor()

    latest_file = get_latest_raw_file()

    with latest_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    jobs = data.get("jobs", [])

    inserted = 0

    for job in jobs:
        source = "remotive"
        source_job_id = str(job["id"])

        cursor.execute(
            """
            INSERT INTO raw_jobs (source, source_job_id, data)
            VALUES (%s, %s, %s)
            ON CONFLICT (source, source_job_id) DO NOTHING
            """,
            (source, source_job_id, json.dumps(job))
        )

        if cursor.rowcount == 1:
            inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ {inserted} jobs insertados en raw_jobs desde {latest_file}")


if __name__ == "__main__":
    load_raw_jobs()