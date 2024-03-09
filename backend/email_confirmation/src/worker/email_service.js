const nodemailer = require('nodemailer');
const config = require('../config');

const transporter = nodemailer.createTransport(config.emailService);

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
