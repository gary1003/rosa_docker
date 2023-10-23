FROM python:3.9 AS builder

COPY . /app

RUN pip install -r /app/requirements.txt

# CMD ["sh", "-c", "python /app/main.py && tail -f /dev/null"]