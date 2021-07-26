#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 10:59:35
# @Author  : 费海瑞
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from config import Config  # 从config模块导入config

app = Flask(__name__)
app.config.from_object(Config)

# 从app包中导入routes
from app import routes