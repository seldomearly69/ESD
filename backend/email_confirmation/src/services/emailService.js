const nodemailer = require('nodemailer');
const amqp = require('amqplib');
const config = require('../config');

const transporter = nodemailer.createTransport(config.emailService);
const RABBITMQ_URL = config.rabbitMQ.url;

async function connectWithRetry(retries = 5, interval = 5000) {
  let connection;

  for (let i = 0; i < retries; i++) {
    try {
      connection = await amqp.connect(RABBITMQ_URL);
      console.log("Connected to RabbitMQ");
      return connection;
    } catch (error) {
      console.error(`Attempt ${i + 1}: Unable to connect to RabbitMQ, retrying in ${interval / 1000} seconds...`, error.message);
      await new Promise(resolve => setTimeout(resolve, interval));
    }
  }

  throw new Error('Failed to connect to RabbitMQ after retries');
}

async function start() {
  try {
    const connection = await connectWithRetry();
    // Proceed with using the connection
    // Here you would typically set up your RabbitMQ channels, exchanges, queues, etc.
  } catch (error) {
    console.error("Fatal error: ", error.message);
    process.exit(1);
  }
}

start();

async function sendEmail(to, subject, text) {
  const mailOptions = { from: config.emailService.auth.user, to, subject, text };
  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent: ' + info.response);
  } catch (error) {
    console.error('Error sending email:', error);
  }
}

module.exports = { sendEmail };
