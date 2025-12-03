FROM python:3.13.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cogs/ ./cogs
COPY services/ ./services
COPY utils/ ./utils
COPY __init__.py .
COPY main.py .

CMD ["python", "main.py"]