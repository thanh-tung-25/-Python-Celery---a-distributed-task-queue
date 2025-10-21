# Dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Default command (Flask) - worker chạy riêng qua docker-compose
CMD ["flask", "run", "--host=0.0.0.0"]
