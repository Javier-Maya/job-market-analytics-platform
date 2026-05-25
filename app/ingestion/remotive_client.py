import requests


REMOTIVE_JOBS_URL = "https://remotive.com/api/remote-jobs"


def fetch_remote_jobs() -> dict:
    """
    Consulta la API de Remotive y devuelve la respuesta JSON
    convertida a un diccionario de Python.
    """
    response = requests.get(REMOTIVE_JOBS_URL, timeout=30)
    response.raise_for_status()

    return response.json()