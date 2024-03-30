FROM node:20
WORKDIR /backend/services/error_handling_service
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5012
CMD ["node", "error_handling.js"]
