from app.db.connection import get_connection


def read_raw_jobs():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT id, data FROM raw_jobs")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    print(f"✅ Se leyeron {len(rows)} registros")

    return rows


if __name__ == "__main__":
    data = read_raw_jobs()
    print(data[0])  # ver primer registro