from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread


# 异步发送电子邮件
# send_async_email()函数现在后台线程中运行
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

from flask_babel import lazy_gettext as _l
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_l('[微博] 重置您的密码'),
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
