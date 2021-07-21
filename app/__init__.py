#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 10:59:35
# @Author  : 费海瑞
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask

app = Flask(__name__)

# 从app包中导入routes
from app import routes