import json

from app.db.connection import get_connection
from app.storage.s3_client import get_latest_json_from_s3


def load_raw_jobs_from_s3():
    """
    Lee el último archivo raw desde S3 y carga los jobs en PostgreSQL.
    """
    data = get_latest_json_from_s3()

    jobs = data.get("jobs", [])

    conn = get_connection()
    cursor = conn.cursor()

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

    print(f"✅ {inserted} jobs insertados en raw_jobs desde S3")


if __name__ == "__main__":
    load_raw_jobs_from_s3()