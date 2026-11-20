FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ikm ./ikm
COPY release ./release
ENV PYTHONPATH=/app IKM_RELEASE_DIR=/app/release
EXPOSE 8000
CMD ["uvicorn", "ikm.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
