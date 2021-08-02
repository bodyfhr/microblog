#-*- coding: UTF-8 -*-
# @Time    : 2021-7-21 11:17:34
# @Author  : 费海瑞
# @File    : microblog.py
# @Software: PyCharm

from app import app, db
from app.models import User, Post
from app import cli


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run(debug=True)