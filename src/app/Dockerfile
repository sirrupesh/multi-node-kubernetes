# Build: Deps only
FROM python:3.13.3-slim as builder
WORKDIR /app
RUN pip install --no-cache-dir flask  # Core pkg

# Run: Minimal image
FROM python:3.13.3-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY app.py /app/

RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser  # Non-root

EXPOSE 5000
CMD ["python", "app.py"]