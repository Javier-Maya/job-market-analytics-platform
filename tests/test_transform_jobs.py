from unittest.mock import patch
from app.processing.transform_jobs import transform_jobs


def test_transform_jobs_maps_fields():
    fake_rows = [
        (1, {"id": "123", "title": "Backend Engineer", "company_name": "Acme"})
    ]

    with patch("app.processing.transform_jobs.read_raw_jobs", return_value=fake_rows):
        result = transform_jobs()

    assert result == [
        {"job_id": "123", "title": "Backend Engineer", "company": "Acme"}
    ]
