from app.db.connection import get_connection


def create_skill_tables():
    conn = get_connection()

    cursor = conn.cursor()

    # Tabla skills
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
    """)

    # Tabla puente
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_skills (
        job_id TEXT,
        skill_id INTEGER,
        PRIMARY KEY (job_id, skill_id)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tablas skills y job_skills creadas")


if __name__ == "__main__":
    create_skill_tables()