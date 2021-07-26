# -*- coding: UTF-8 -*-
# @Time    : 2021-7-23 16:28:00
# @Author  : 费海瑞
# @File    : config.py
# @Software: PyCharm

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
