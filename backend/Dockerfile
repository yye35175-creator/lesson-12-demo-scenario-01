FROM python:3.14-slim
WORKDIR /backend
COPY backend/pyproject.toml ./
COPY backend/app ./app
RUN python -m pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
