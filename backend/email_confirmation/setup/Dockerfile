# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pika package for RabbitMQ
RUN pip install pika

# Make port 5672 available to the world outside this container
# This is the default port for RabbitMQ
EXPOSE 5672

# Run amqp_setup.py when the container launches
CMD ["python", "./amqp_setup.py"]