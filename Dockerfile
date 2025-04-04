FROM python:3.11

ENV VENV "/venv"
ENV PATH "${VENV}/bin:${PATH}"
ENV PYTHONPATH "${PYTHONPATH}:/opt/backend"

WORKDIR /opt/backend

COPY pyproject.toml poetry.lock ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]