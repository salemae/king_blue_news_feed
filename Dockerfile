# Use the official Python image as the base image
FROM python:3.8

# Set environment variables
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY app.py .
COPY templates templates
COPY subscribers.db .

# Install required Python packages
RUN pip install flask feedparser

# Expose the port your Flask app will run on
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run"]
