# Multi-stage build for optimized Flask application container
# Stage 1: Dependencies installation
FROM python:3.13.3-slim as builder
WORKDIR /app
RUN pip install --no-cache-dir flask  # Install minimal dependencies, no cache for smaller image

# Stage 2: Final runtime image
FROM python:3.13.3-slim
WORKDIR /app
# Copy only the installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY app.py /app/

# Security: Create non-root user and set permissions
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser  # Run as non-privileged user for security

EXPOSE 5000  # Application port for container networking
CMD ["python", "app.py"]  # Start the Flask application