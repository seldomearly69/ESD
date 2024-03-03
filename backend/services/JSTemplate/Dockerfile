# Use an official Node.js runtime as a parent image
FROM node:21.6.2

# Set the working directory in the container
WORKDIR /backend/services/JSTemplate

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Bundle app source
COPY . .

# Expose the port on which your app will run
EXPOSE 5005

# Define the command to run your application
CMD [ "node", "JSTemplate.js" ]

