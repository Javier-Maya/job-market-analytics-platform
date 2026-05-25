import json
import os
import boto3
from pathlib import Path


def upload_file_to_s3(local_file: Path, s3_key: str) -> None:
    """
    Sube un archivo local a un bucket S3.
    """
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        raise ValueError("La variable S3_BUCKET_NAME no está definida")

    s3 = boto3.client("s3")

    s3.upload_file(
        Filename=str(local_file),
        Bucket=bucket_name,
        Key=s3_key
    )

    print(f"✅ Archivo subido a S3: s3://{bucket_name}/{s3_key}")


def get_latest_json_from_s3() -> dict:
    """
    Busca el último archivo JSON subido a S3 en raw/remotive/,
    lo descarga y lo devuelve como diccionario de Python.
    """
    bucket_name = os.getenv("S3_BUCKET_NAME")
    prefix = "raw/remotive/"

    if not bucket_name:
        raise ValueError("La variable S3_BUCKET_NAME no está definida")

    s3 = boto3.client("s3")

    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix
    )

    files = response.get("Contents", [])

    json_files = [
        file for file in files
        if file["Key"].endswith(".json")
    ]

    if not json_files:
        raise FileNotFoundError(f"No se encontraron archivos JSON en s3://{bucket_name}/{prefix}")

    latest_file = max(
        json_files,
        key=lambda file: file["LastModified"]
    )

    latest_key = latest_file["Key"]

    s3_object = s3.get_object(
        Bucket=bucket_name,
        Key=latest_key
    )

    content = s3_object["Body"].read().decode("utf-8")
    data = json.loads(content)

    print(f"✅ Archivo leído desde S3: s3://{bucket_name}/{latest_key}")

    return data