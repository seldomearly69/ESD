FROM node:20
WORKDIR /backend/services/plan_route
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5013
CMD ["node", "plan_route.js"]