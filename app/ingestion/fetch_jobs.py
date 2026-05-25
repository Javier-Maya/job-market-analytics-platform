from app.ingestion.remotive_client import fetch_remote_jobs
from app.ingestion.save_raw import save_raw_jobs


def fetch_jobs():
    print("Iniciando ingesta de jobs desde Remotive...")

    data = fetch_remote_jobs()

    file_path = save_raw_jobs(data)

    print(f"Ingesta finalizada correctamente. Archivo guardado en: {file_path}")


if __name__ == "__main__":
    fetch_jobs()