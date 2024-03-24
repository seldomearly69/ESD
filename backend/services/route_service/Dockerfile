FROM node:latest
WORKDIR /backend/services/route_service
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "route_service.js"]