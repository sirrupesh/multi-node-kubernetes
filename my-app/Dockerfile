# Use an official Python runtime as the base image
FROM python:3.13.3-slim
 
# Set the working directory
WORKDIR /app
 
# Copy application files
COPY app.py /app
 
# Copy requirements and install dependencies
RUN pip install flask
 
# Expose the application port
EXPOSE 5000
 
# Run the application
CMD ["python", "app.py"]