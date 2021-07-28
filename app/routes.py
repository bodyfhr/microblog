#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:14:14
# @Author  : 费海瑞
# @File    : routes.py
# @Software: PyCharm
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import RegistrationForm
from app import db
from app.forms import EditProfileForm

# 主页路由
@app.route('/')
@app.route('/index')
@login_required
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
@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   login_form = LoginForm()  # 表单实例化对象
   if login_form.validate_on_submit():
      user = User.query.filter_by(username=login_form.username.data).first()
      if user is None or not user.check_password(login_form.password.data):
         flash('Invalid username or password')
         return redirect(url_for('login'))
      login_user(user, remember=login_form.remember_me.data)
      # 重定向到next页面
      next_page = request.args.get('next')
      if not next_page or url_parse(next_page).netloc != '':
         next_page = url_for('index')
      return redirect(next_page)
      # msg = 'Login requested for user {},remember_me={}'.format(login_form.username.data, login_form.remember_me.data)
      # flash(msg)
      # print(msg)
      # return redirect(url_for('index'))
   return render_template('login.html', title='Sign In', form=login_form)


# 退出登录路由
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))


# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
      user = User(username=form.username.data, email=form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Congratulations, you are now a registered user!')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)


# 用户个人资料路由
@app.route('/user/<username>')
@login_required
def user(username):
   user = User.query.filter_by(username=username).first_or_404()
   posts = [
      {'author': user, 'body': 'Test post #1'},
      {'author': user, 'body': 'Test post #2'}
   ]
   return render_template('user.html', user=user, posts=posts)


# 记录用户上次访问时间路由
@app.before_request
def before_request():
   if current_user.is_authenticated:
      current_user.last_seen = datetime.utcnow()
      db.session.commit()


# 个人资料编辑路由
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
   form = EditProfileForm()
   if form.validate_on_submit():
      current_user.username = form.username.data
      current_user.about_me = form.about_me.data
      db.session.commit()

      flash('Your changes have been saved.')
      return redirect(url_for('edit_profile'))
   elif request.method == 'GET':
      form.username.data = current_user.username
      form.about_me.data = current_user.about_me
   return render_template('edit_profile.html', title='Edit Profile', form=form)
