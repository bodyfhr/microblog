# -*- coding: UTF-8 -*-
# @Time    : 2021-7-29 11:15:53
# @Author  : 费海瑞
# @File    : email.py
# @Software: PyCharm

from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread
from flask_babel import _


# 异步发送电子邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 发送电子邮件
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


# 发送密码重置电子邮件
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
