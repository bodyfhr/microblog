#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:14:14
# @Author  : 费海瑞
# @File    : routes.py
# @Software: PyCharm
from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm


# 主页路由
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


# 登录路由
@app.route('/loginxxx', methods=['GET', 'POST'])
def login():
   login_form = LoginForm()  # 表单实例化对象
   if login_form.validate_on_submit():
      msg = 'Login requested for user {},remember_me={}'.format(login_form.username.data, login_form.remember_me.data)
      flash(msg)
      print(msg)
      return redirect(url_for('index'))
   return render_template('login.html', title='Sign In', form=login_form)
