from flask.ext.mail import Message
from flask import render_template
from app import mail, app
from config import ADMINS
#import threading
#from threading import Thread
from decorators import async

@async
def send_async_email(msg):
    app.logger.debug('prepare sending email')
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)
#    thr = threading.Thread(target = send_async_email, args = [msg]) # use @aync decorator so not need.
#    thr.start()

def follower_notification(followed, follower):
    send_email("[miniblog] %s is now following you!" % follower.nickname,
            ADMINS[1], [followed.email],
            render_template("follower_email.txt", user = followed, follower = follower),
            render_template("follower_email.html", user = followed, follower = follower))
