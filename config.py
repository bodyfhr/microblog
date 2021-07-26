# -*- coding: UTF-8 -*-
# @Time    : 2021-7-23 16:28:00
# @Author  : 费海瑞
# @File    : config.py
# @Software: PyCharm

import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前.py文件的绝对路径

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s/%s" % ('root', 'root', '127.0.0.1', 'flask_blog')
    SQLALCHEMY_TRACK_MODIFICATONS = False
