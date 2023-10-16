FROM python:3.9 AS builder

COPY . /app

RUN pip install -r /app/requirements.txt

# CMD ["bash"]
CMD ["python", "/app/main.py"]