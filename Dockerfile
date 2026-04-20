FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# cache-bust-v2
COPY . .

CMD ["python", "-u", "run.py"]
