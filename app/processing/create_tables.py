from app.db.connection import get_connection


def create_tables():
    conn = get_connection()

    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS raw_jobs (
        id SERIAL PRIMARY KEY,
        source TEXT NOT NULL,
        source_job_id TEXT NOT NULL,
        data JSONB NOT NULL,
        loaded_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (source, source_job_id)
    );
    """

    cursor.execute(create_table_query)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tabla raw_jobs creada correctamente")

if __name__ == "__main__":
    create_tables()