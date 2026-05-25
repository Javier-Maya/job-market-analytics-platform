import boto3
import json
from datetime import datetime


def upload_sample_json():
    s3 = boto3.client("s3")

    bucket_name = "job-market-raw-javier-2026"

    # JSON de prueba
    data = {
        "message": "Hola S3",
        "timestamp": datetime.now().isoformat()
    }

    file_name = f"raw/test/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data)
    )

    print(f"Archivo subido correctamente a S3: {file_name}")


if __name__ == "__main__":
    upload_sample_json()