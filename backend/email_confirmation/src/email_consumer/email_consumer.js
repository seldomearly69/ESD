const amqp = require('amqplib');
const { sendEmail } = require('../services/emailService');
const config = require('../config');

async function startConsumer() {
  const conn = await amqp.connect(config.rabbitMQ.url);
  const channel = await conn.createChannel();
  const queue = 'bookingCompletionQueue';

  await channel.assertQueue(queue, { durable: false });
  console.log("Waiting for messages in %s. To exit press CTRL+C", queue);

  channel.consume(queue, (msg) => {
    const { email, subject, text } = JSON.parse(msg.content.toString());
    sendEmail(email, subject, text);
  }, { noAck: true });
}

startConsumer().catch(console.error);
