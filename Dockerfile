FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY calculator_api ./calculator_api

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "calculator_api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]