from app.db.connection import get_connection

def count_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clean_jobs;")
    total = cursor.fetchone()[0]

    print(f"Total jobs in clean_jobs: {total}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    count_jobs()