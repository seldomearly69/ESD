FROM node:20
WORKDIR /backend/services/route_service
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5006
CMD ["node", "route_service.js"]