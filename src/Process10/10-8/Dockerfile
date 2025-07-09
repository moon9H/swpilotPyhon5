# 과정 10 - (문제8) 집으로 가는 길
FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY main_api.py .
COPY iris_model.pkl .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]