# -*- coding: UTF-8 -*-
# @Time    : 2021-8-4 17:01:58
# @Author  : 费海瑞
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes

