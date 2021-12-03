# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /usr/src/faicorn/apis
WORKDIR /usr/src/faicorn/apis

COPY installed_app.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ./installed_app.txt

COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -Rp appuser /ksave/apis/kreadorapis/paymentapi
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug

# CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
