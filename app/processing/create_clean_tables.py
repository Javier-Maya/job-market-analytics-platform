from app.db.connection import get_connection


def create_clean_tables():
    conn = get_connection()

    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS clean_jobs (
        id SERIAL PRIMARY KEY,
        source TEXT NOT NULL,
        source_job_id TEXT NOT NULL,
        title TEXT,
        company TEXT,
        job_type TEXT,
        location TEXT,
        publication_date TIMESTAMP,
        UNIQUE (source, source_job_id)
    );
    """

    cursor.execute(create_table_query)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tabla clean_jobs creada correctamente")


if __name__ == "__main__":
    create_clean_tables()