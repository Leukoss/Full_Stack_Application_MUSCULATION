# Use the official Python image from the Docker Hub
FROM python:3.12

# Set environment variables
# Keep smaller size for the container
ENV PYTHONDONTWRITEBYTECODE 1
# Output directly sent to the terminal
ENV PYTHONUNBUFFERED 1
# Database Conneciton Configuration
ENV DATABASE_URL=postgres://admin:12345@db:5432/workout_db

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port on which the app runs
EXPOSE 8080
