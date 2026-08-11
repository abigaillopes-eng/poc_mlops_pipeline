FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./

COPY calculator_api/src ./src

RUN python -m pip install --upgrade pip --root-user-action=ignore \
    && python -m pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]