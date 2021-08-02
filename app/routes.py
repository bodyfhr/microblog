#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:14:14
# @Author  : 费海瑞
# @File    : routes.py
# @Software: PyCharm
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app.forms import RegistrationForm
from app import db
from app.forms import EditProfileForm
from app.email import send_password_reset_email
from flask_babel import _


# 主页路由
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
   form = PostForm()
   if form.validate_on_submit():
      post = Post(body=form.post.data, author=current_user)
      db.session.add(post)
      db.session.commit()
      flash(_('Your post is now live!'))
      return redirect(url_for('index'))
   # 创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
   page = request.args.get('page', 1, type=int)
   posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('index', page=posts.next_num) if posts.has_next else None
   prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
   return render_template('index.html', title='Home Page', form=form, posts=posts.items, next_url=next_url,
                          prev_url=prev_url)


# 显示自己和自己关注的帖子
@app.route('/explore')
@login_required
def explore():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
   prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
   return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   login_form = LoginForm()  # 表单实例化对象
   if login_form.validate_on_submit():
      user = User.query.filter_by(username=login_form.username.data).first()
      if user is None or not user.check_password(login_form.password.data):
         flash(_('Invalid username or password'))
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
      flash(_('Congratulations, you are now a registered user!'))
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)


# 重置密码路由
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = ResetPasswordRequestForm()
   if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user:
         send_password_reset_email(user)
      flash(_('Check your email for the instructions to reset your password'))
      return redirect(url_for('login'))
   return render_template('reset_password_request.html', title='Reset Password', form=form)


# 重置用户密码路由
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
   if current_user.is_authenticated:
      return render_template(url_for('index'))
   user = User.verify_reset_password_token(token)
   if not user:
      return redirect(url_for('index'))
   form = ResetPasswordForm()
   if form.validate_on_submit():
      user.set_password(form.password.data)
      db.session.commit()
      flash(_('Your password has been reset.'))
      return redirect(url_for('login'))
   return render_template('reset_password.html', form=form)


# 用户个人资料路由
@app.route('/user/<username>')
@login_required
def user(username):
   user = User.query.filter_by(username=username).first_or_404()
   page = request.args.get('page', 1, type=int)
   posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
   prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
   return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


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

      flash(_('Your changes have been saved.'))
      return redirect(url_for('edit_profile'))
   elif request.method == 'GET':
      form.username.data = current_user.username
      form.about_me.data = current_user.about_me
   return render_template('edit_profile.html', title='Edit Profile', form=form)


# 关注路由
@app.route('/follow/<username>')
@login_required
def follow(username):
   user = User.query.filter_by(username=username).first()
   if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('index'))
   if user == current_user:
      flash(_('You cannot follow yourself!'))
      return redirect(url_for('user', username=username))
   current_user.follow(user)
   db.session.commit()
   flash(_('You are following %{username}!', username=username))
   return redirect(url_for('user', username=username))


# 取消关注路由
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
   user = User.query.filter_by(username=username).first()
   if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('index'))
   if user == current_user:
      flash(_('You cannot unfollow yourself!'))
      return redirect(url_for('user', username=username))
   current_user.unfollow(user)
   db.session.commit()
   flash(_('You are following %{username}!', username=username))
   return redirect(url_for('user', username=username))
