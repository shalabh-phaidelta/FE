# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the port used by NiceGUI
EXPOSE 8080

# Run the NiceGUI app
CMD ["python", "nicegui_app/app.py"]
