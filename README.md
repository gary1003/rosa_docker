# ROSA DOCKER EXAMPLE

This is a ROSA example that uses Docker to build and deploy a simple application.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)

## DOCKERFILE

The Dockerfile is used to build the application image.
This example uses a simple Python application use boto3 to check new data in dynamodb, and send it to line notify.

```dockerfile
FROM python:3.9 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app .

CMD ["python", "main.py"]
```

## Local test

```bash
docker build -t <image_name> .
docker run -it --rm -p <image_name>
```

## deploy

```bash
crontab -e
```

```bash
* * * * * docker run -it --rm -p <image_name>
```
