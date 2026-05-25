from app.processing.read_raw_jobs import read_raw_jobs


def transform_jobs():
    rows = read_raw_jobs()

    transformed = []

    for row in rows:
        raw_id, data = row

        job_id = data.get("id")
        title = data.get("title")
        company = data.get("company_name")

        transformed.append({
            "job_id": job_id,
            "title": title,
            "company": company
        })

    print("✅ Transformación lista")
    print(transformed[0])  # ver ejemplo

    return transformed


if __name__ == "__main__":
    transform_jobs()