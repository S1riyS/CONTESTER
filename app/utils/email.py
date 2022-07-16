from flask_mail import Message
from app import mail


def send_email(subject, recipients, text_body=None, html_body=None):
    message = Message(subject, recipients=recipients)
    if text_body:
        message.body = text_body
    if html_body:
        message.html = html_body
    mail.send(message)
