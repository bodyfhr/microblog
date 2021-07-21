#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:14:14
# @Author  : 费海瑞
# @File    : routes.py
# @Software: PyCharm

from app import app

@app.route('/')
@app.route('/index')
def index():
   return "Hello World!"