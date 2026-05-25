from datetime import datetime

from app.db.connection import get_connection
from app.processing.read_raw_jobs import read_raw_jobs


def parse_publication_date(value: str | None):
    """
    Convierte la fecha del JSON a datetime de Python.
    Si no existe o falla, devuelve None.
    """
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_clean_jobs():
    rows = read_raw_jobs()

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0

    for row in rows:
        _, data = row

        source = "remotive"
        source_job_id = str(data.get("id"))
        title = data.get("title")
        company = data.get("company_name")
        job_type = data.get("job_type")
        location = data.get("candidate_required_location")
        publication_date = parse_publication_date(data.get("publication_date"))

        cursor.execute(
            """
            INSERT INTO clean_jobs (
                source,
                source_job_id,
                title,
                company,
                job_type,
                location,
                publication_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source, source_job_id) DO NOTHING
            """,
            (
                source,
                source_job_id,
                title,
                company,
                job_type,
                location,
                publication_date
            )
        )

        if cursor.rowcount == 1:
            inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ {inserted} registros insertados en clean_jobs")


if __name__ == "__main__":
    load_clean_jobs()
