# Imagen base con Python
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias
COPY requirements.txt .

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto al contenedor
COPY . .

# Puerto donde correrá FastAPI
EXPOSE 8000

# Comando para levantar la API
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
