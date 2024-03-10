# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install dependencies required for wait-for-it.sh
RUN apt-get update && apt-get install -y --no-install-recommends wait-for-it

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Copy wait-for-it.sh into the container
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port available to the world outside this container
EXPOSE 5002

# Define environment variable
ENV NAME World

# Use wait-for-it.sh to check for RabbitMQ availability before starting the service
CMD /wait-for-it.sh rabbitmq:5672 -- python app.py
