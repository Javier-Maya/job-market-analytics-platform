import json
from datetime import datetime
from pathlib import Path

from app.storage.s3_client import upload_file_to_s3


RAW_DATA_DIR = Path("data/raw")


def save_raw_jobs(data: dict) -> Path:
    """
    Guarda la respuesta cruda de la API en un archivo JSON
    dentro de data/raw y también la sube a S3.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"jobs_raw_{timestamp}.json"
    output_file = RAW_DATA_DIR / file_name

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    s3_key = f"raw/remotive/{file_name}"
    upload_file_to_s3(output_file, s3_key)

    return output_file