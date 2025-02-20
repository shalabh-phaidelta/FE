# Use Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy NiceGUI app files
COPY . .

# Expose NiceGUI UI port
EXPOSE 8080

# Run NiceGUI app
CMD ["python", "ui_app.py"]
