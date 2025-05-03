# Multi-stage Flask app build
# Stage 1: Dependencies
FROM python:3.13.3-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13.3-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY src/ /app/

# Security: Non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000  # App port
EXPOSE 9090  # Metrics port

CMD ["python", "app.py"]