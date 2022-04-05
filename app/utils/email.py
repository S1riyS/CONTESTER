from flask_mail import Message
from app import app, mail


def send_email(subject, recipients, text_body, html_body):
    message = Message(subject, recipients=recipients)
    message.body = text_body
    message.html = html_body
    mail.send(message)
