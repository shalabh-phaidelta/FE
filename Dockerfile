# Use the official Python image as a base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/



# Expose port 8501 (default port for Streamlit)
EXPOSE 8501


# Command to run Streamlit when the container starts

# Use the full path to Streamlit in CMD
CMD ["streamlit", "run", "/app/Weather_App_V2.py"]
