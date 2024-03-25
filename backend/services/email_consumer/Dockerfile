# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Ensure you have Flask, pika, and any other dependencies listed in your requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt
# Define environment variables for email credentials
# Replace these with your actual email and password or use Docker secrets for production environments
ENV EMAIL_USER=booking.t4.g6@gmail.com
ENV EMAIL_PASSWORD=aggyeynwnrpvvcqc

ENV FLASK_APP=app.py
# Run app.py when the container launches
CMD ["python", "./app.py"]
