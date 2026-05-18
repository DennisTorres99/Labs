FROM python:3.12-slim AS builder

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
