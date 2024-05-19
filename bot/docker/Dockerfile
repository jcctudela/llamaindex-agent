# Usar una imagen oficial de Python como imagen base
FROM python:3.10-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema necesarias
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# Instalar dependencias de Python

RUN pip install --upgrade pip

WORKDIR /app
COPY ./requirements /app/requirements
RUN pip install -r requirements/base.txt

