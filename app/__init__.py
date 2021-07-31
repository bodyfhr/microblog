#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 10:59:35
# @Author  : 费海瑞
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from flask_mail import Mail

from config import Config  # 从config模块导入config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)  # 数据库对象
migrate = Migrate(app, db)  # 迁移引擎对象
login = LoginManager(app)  # 登录设置
login.login_view = 'login'

mail = Mail(app)

# 从app包中导入routes
from app import routes, models
