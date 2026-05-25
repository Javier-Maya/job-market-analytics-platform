from app.db.connection import get_connection
from app.processing.read_raw_jobs import read_raw_jobs


def load_skills():
    rows = read_raw_jobs()

    conn = get_connection()

    cursor = conn.cursor()

    for row in rows:
        _, data = row

        job_id = str(data.get("id"))

        # Obtener lista de skills desde JSON
        tags = data.get("tags", [])

        for tag in tags:
            skill_name = tag.strip()

            # 2. Insertar skill si no existe
            cursor.execute(
                """
                INSERT INTO skills (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                """,
                (skill_name,)
            )

            # 3. Obtener ID de la skill
            cursor.execute(
                """
                SELECT id FROM skills WHERE name = %s
                """,
                (skill_name,)
            )

            result = cursor.fetchone()
            skill_id = result[0]

            # 4. Insertar relación
            cursor.execute(
                """
                INSERT INTO job_skills (job_id, skill_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (job_id, skill_id)
            )

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Skills y relaciones cargadas correctamente")


if __name__ == "__main__":
    load_skills()