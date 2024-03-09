
FROM node:14


WORKDIR /usr/src/app


COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "src/email_consumer/email_consumer.js"]
