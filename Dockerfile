# Use a small Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies (if requirements.txt exists)
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

# Default command when container runs
CMD ["python3"]
