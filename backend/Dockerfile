FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV LOG_LEVEL=INFO

COPY . .

EXPOSE 8000

# RUN mkdir -p /app/logs && chmod -R 777 logs

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
