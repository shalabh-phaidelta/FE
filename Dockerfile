# Use official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
