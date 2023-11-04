#!/bin/bash

# Kingblue Installation Script

# Check if the script is running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root."
  exit 1
fi

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
  echo "Docker is not installed or not running."
  echo "Please install Docker and make sure it is running before proceeding."
  exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Python is not installed."
  echo "Please install Python before proceeding."
  exit 1
fi

# Give the user the option to choose between Docker or Local Install
echo "Choose an installation method for Kingblue:"
echo "1. Docker Install"
echo "2. Local Install"
read -p "Enter your choice (1/2): " choice

if [ "$choice" == "1" ]; then
  # Docker Install
  echo "Starting Docker Install for Kingblue..."
  
  # Build the Docker image
  docker build -t kingblue .

  # Run the Docker container in the background
  docker run -d -p 8888:5000 kingblue

  echo "Kingblue Docker container is now running in the background."
  echo "Access Kingblue at: http://localhost:8888"
  echo "Default login credentials for Kingblue: Username: admin, Password: admin"

elif [ "$choice" == "2" ]; then
  # Local Install
  echo "Starting Local Install for Kingblue..."
  
  # Create a Python virtual environment
  python3 -m venv venv

  # Activate the virtual environment
  source venv/bin/activate

  # Install the required packages from requirements.txt
  pip install -r requirements.txt

  # Run the Kingblue app
  python app.py

  # Deactivate the virtual environment
  deactivate

  echo "Local installation for Kingblue completed."
  echo "Access Kingblue at: http://localhost:5000"
  echo "Default login credentials for Kingblue: Username: admin, Password: admin"

else
  echo "Invalid choice. Please choose 1 for Docker Install or 2 for Local Install."
  exit 1
fi
