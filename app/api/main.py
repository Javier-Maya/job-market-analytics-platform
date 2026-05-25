from fastapi import FastAPI, HTTPException

from app.db.connection import get_connection


app = FastAPI()


def get_db_connection():
    return get_connection()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/jobs")
def get_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_job_id, title, company, job_type, location, publication_date
        FROM clean_jobs
        LIMIT 20
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    jobs = []

    for row in rows:
        jobs.append({
            "source_job_id": row[0],
            "title": row[1],
            "company": row[2],
            "job_type": row[3],
            "location": row[4],
            "publication_date": row[5]
        })

    return jobs


@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_job_id, title, company, job_type, location, publication_date
        FROM clean_jobs
        WHERE source_job_id = %s
    """, (job_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")

    job = {
        "source_job_id": row[0],
        "title": row[1],
        "company": row[2],
        "job_type": row[3],
        "location": row[4],
        "publication_date": row[5]
    }

    return job


@app.get("/skills")
def get_skills():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM skills
        ORDER BY name
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    skills = []

    for row in rows:
        skills.append({
            "id": row[0],
            "name": row[1]
        })

    return skills


@app.get("/skills/top")
def get_top_skills():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.name, COUNT(js.job_id) AS job_count
        FROM skills s
        JOIN job_skills js ON s.id = js.skill_id
        GROUP BY s.name
        ORDER BY job_count DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    top_skills = []

    for row in rows:
        top_skills.append({
            "skill": row[0],
            "job_count": row[1]
        })

    return top_skills