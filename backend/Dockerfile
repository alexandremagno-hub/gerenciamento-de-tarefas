FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --without dev --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi_zero.app:app", "--host", "0.0.0.0", "--port", "8000"]
