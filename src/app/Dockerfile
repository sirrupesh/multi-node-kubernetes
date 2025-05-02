# Multi-stage build for Python Flask application
# Stage 1: Build environment
FROM python:3.13.3-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies and Flask
RUN pip install --no-cache-dir flask

# Stage 2: Runtime environment
FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Copy only the necessary files from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY app.py /app/

# Set non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]