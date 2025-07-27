FROM python:3.10.2-slim-buster
WORKDIR /app

# Only copy requirements first, to leverage caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9100

ENTRYPOINT ["python", "./server.py"]
