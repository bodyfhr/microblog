# -*- coding: UTF-8 -*-
# @Time    : 2021-7-26 09:48:15
# @Author  : 费海瑞
# @File    : forms.py
# @Software: PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


# 个人资料编辑
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About_me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))


# 博客提交表单
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))
