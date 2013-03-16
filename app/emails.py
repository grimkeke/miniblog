from flask.ext.mail import Message
from flask import render_template
from app import mail
from config import ADMINS
from threading import Thread

def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender, recipients)
    msg.body = text_body
    msg.html = html_body
    thr = threading.Thread(target = send_async_email, args = [msg])
    thr.start()

def follower_notification(followed, follower):
    send_email("[miniblog] %s is now following you!" % follower.nickname,
            ADMINS[1], [followed.email],
            render_template("follower_email.txt", user = followed, follower = follower),
            render_template("follower_email.html", user = followed, follower = follower))
