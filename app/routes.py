#!/usr/bin/env python # -*- coding:utf-8 -*-
from app import app#从app包导入init中app对象


#定义路由 这里定义了2个路由
@app.route('/')
@app.route('/index')
def index():
    return 'hrello hongkong'