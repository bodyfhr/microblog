# -*- coding: UTF-8 -*-
# @Time    : 2021-8-4 17:20:53
# @Author  : 费海瑞
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
