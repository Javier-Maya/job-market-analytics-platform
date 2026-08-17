from app.ingestion.fetch_jobs import fetch_jobs
from app.ingestion.load_raw_jobs_from_s3 import load_raw_jobs_from_s3
from app.processing.load_clean_jobs import load_clean_jobs
from app.processing.load_skills import load_skills

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("🚀 Iniciando pipeline completo...")

    logger.info("📡 Paso 1: Ingesta desde Remotive → S3")
    fetch_jobs()

    logger.info("🗄️ Paso 2: Carga desde S3 → PostgreSQL raw_jobs")
    load_raw_jobs_from_s3()

    logger.info("🧹 Paso 3: Transformación raw_jobs → clean_jobs")
    load_clean_jobs()

    logger.info("🧠 Paso 4: Modelado skills + job_skills")
    load_skills()

    logger.info("✅ Pipeline finalizado correctamente")


if __name__ == "__main__":
    run_pipeline()