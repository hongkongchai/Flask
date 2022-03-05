#!/usr/bin/env python # -*- coding:utf-8 -*-
from app import app#从app包导入init中app对象
from flask import render_template


#定义路由 这里定义了2个路由
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'hongkong'}
    age = {'age':'23'}
    sex = {'sex':'男'}

    posts = [#创建一个列表：帖子，里面元素是两个字典，每个字典李元素还是字典，分别作者，帖子内容
        {
            'author': {'username': 'hk1'},
            'body': '漂亮，美丽'
        },
        {
            'author': {'username': 'hk2'},
            'body': '大方，尊贵'
        }
    ]
    return render_template('index.html', title='Home-hk', user=user, age=age, sex=sex, posts=posts)
