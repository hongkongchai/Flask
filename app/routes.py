#!/usr/bin/env python # -*- coding:utf-8 -*-
from app import app#从app包导入init中app对象
from flask import render_template, url_for
from app.forms import LoginForm
from flask import render_template,flash,redirect
from flask_login import current_user,login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm


#定义路由 这里定义了2个路由
@app.route('/')
@app.route('/index')
#装饰器拦截请求，要求用户登录
@login_required
def index():
    posts = [#创建一个列表：帖子，里面元素是两个字典，每个字典李元素还是字典，分别作者，帖子内容
        {
            'author': {'username': 'hk1'},
            'body': '漂亮，美丽'
        },
        {
            'author': {'username': 'hk2'},
            'body': '大方，尊贵'
        },        {
            'author': {'username': 'hk2'},
            'body': '大方，尊贵'
        }
    ]
    return render_template('index.html', title='Home-hk', posts=posts)

#用户登录
@app.route('/login',methods=['GET','POST'])
def login():
    #current_user表示请求客户端的用户对象   尚未注册则是匿名用户对象  is_authenticated可以检查用户导航到/login，判断用户是否已登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

#    login_form = LoginForm()#表单实例化对象
#    msg='Login request for user {},remember_me={}'.format(login_form.username.data, login_form.remember_me.data)
    if login_form.validate_on_submit():
#        flash(msg)
#        print(msg)
        #filter_by（）查询对象，等到的结果只包含匹配用户名的对象，调用first()完成查询如果存在返回用户对象，否则为none，调用all()全部查询，当我们只需要一个结果时调用first()
        user = User.query.filter_by(username=login_form.username.data).first()
        #check_password检查表单附带的密码是否有效
        if user is None or not user.check_password(login_form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user,remember=login_form.remember_me.data)

        #return redirect('/index')#重定向
        #重定向到next页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='login', form=login_form)

#用户退出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#注册
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
        flash('恭喜你，你现在已经是注册用户了!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)