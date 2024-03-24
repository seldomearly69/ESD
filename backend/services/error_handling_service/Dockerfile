FROM node:latest
WORKDIR /backend/services/error_handling_service
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "error_handling.js"]
