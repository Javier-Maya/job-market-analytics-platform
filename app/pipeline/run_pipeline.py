from app.ingestion.fetch_jobs import fetch_jobs
from app.ingestion.load_raw_jobs_from_s3 import load_raw_jobs_from_s3
from app.processing.load_clean_jobs import load_clean_jobs
from app.processing.load_skills import load_skills


def run_pipeline():
    print("🚀 Iniciando pipeline completo...")

    print("\n📡 Paso 1: Ingesta desde Remotive → S3")
    fetch_jobs()

    print("\n🗄️ Paso 2: Carga desde S3 → PostgreSQL raw_jobs")
    load_raw_jobs_from_s3()

    print("\n🧹 Paso 3: Transformación raw_jobs → clean_jobs")
    load_clean_jobs()

    print("\n🧠 Paso 4: Modelado skills + job_skills")
    load_skills()

    print("\n✅ Pipeline finalizado correctamente")


if __name__ == "__main__":
    run_pipeline()