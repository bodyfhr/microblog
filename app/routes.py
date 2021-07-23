#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:14:14
# @Author  : 费海瑞
# @File    : routes.py
# @Software: PyCharm
from flask import render_template

from app import app

@app.route('/')
@app.route('/index')
def index():
   user = {'username':'songbo'}
   # 创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
   posts = [
      {
         'author': {'username': 'John'},
         'body': 'Beautiful day in Portland!'
      },
      {
      'author': {'username': 'Susan'},
      'body': 'The Avengers movie was so cool!'
      }
   ]
   return render_template("index.html",title='home',user=user,posts=posts)