#!/usr/bin/env python # -*- coding:utf-8 -*-
from guess_language import guess_language

from app import app  # 从app包导入init中app对象
from flask import render_template, url_for, jsonify

from app.cli import translate
from app.forms import LoginForm, PostForm
from flask import render_template, flash, redirect
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
from app.models import Post
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
from werkzeug.urls import url_parse
from flask_babel import _
from flask import g
from flask_babel import get_locale


# 定义路由 这里定义了2个路由
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# 装饰器拦截请求，要求用户登录
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('你的帖子现在是实时的!'))
        return redirect(url_for('index'))
    posts = current_user.followed_posts().all()

    # 分页
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home Page', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


# 视图函数
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user表示请求客户端的用户对象   尚未注册则是匿名用户对象  is_authenticated可以检查用户导航到/login，判断用户是否已登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    #    login_form = LoginForm()#表单实例化对象
    #    msg='Login request for user {},remember_me={}'.format(login_form.username.data, login_form.remember_me.data)
    if login_form.validate_on_submit():
        #        flash(msg)
        #        print(msg)
        # filter_by（）查询对象，等到的结果只包含匹配用户名的对象，调用first()完成查询如果存在返回用户对象，否则为none，调用all()全部查询，当我们只需要一个结果时调用first()
        user = User.query.filter_by(username=login_form.username.data).first()
        # check_password检查表单附带的密码是否有效
        if user is None or not user.check_password(login_form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)

        # return redirect('/index')#重定向
        # 重定向到next页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='login', form=login_form)


# 用户退出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# 注册
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


# 找回密码
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('请检查您的电子邮件，以获取重置密码的说明')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


# 重置密码
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('您的密码已经重置.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


# 用户个人资料的视图函数
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


# 记录用户上次访问时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # g.locale = str(get_locale())
        g.locale = 'zh_CN' if str(get_locale()).startswith('zh') else str(get_locale())


# 文本翻译视图函数
@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify(
        {'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])})


# 编辑个人资料
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # form = EditProfileForm()
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('您的更改已经保存.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)
