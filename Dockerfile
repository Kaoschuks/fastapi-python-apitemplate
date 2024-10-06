# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.10-slim-buster
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 8000

# for production
# RUN apt-get update && apt-get install -y python3-dev build-essential
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -Rp appuser /usr/src/aideapis/coreapi
# USER appuser

RUN mkdir -p /usr/src/aideapis/coreapi
WORKDIR /usr/src/aideapis/coreapi

COPY installed_apps.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ./installed_apps.txt

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# for production
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "20", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
