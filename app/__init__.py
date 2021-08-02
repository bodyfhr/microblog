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
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask import request
from flask_babel import Babel, lazy_gettext as _l

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)  # 数据库对象
migrate = Migrate(app, db)  # 迁移引擎对象
login = LoginManager(app)  # 登录设置
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

mail = Mail(app)  # 发送邮件
bootstrap = Bootstrap(app)  # Bootstrap美化站点
moment = Moment(app)  # 处理日期和时间
babel = Babel(app)  # 国际化和本地化


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# 从app包中导入routes
from app import routes, models
