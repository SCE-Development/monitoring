FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir prometheus-client

COPY push_metrics.py .

CMD ["python", "push_metrics.py"]
