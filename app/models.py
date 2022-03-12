#!/usr/bin/env python # -*- coding:utf-8 -*-

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from flask_login import UserMixin


#关注者关联表
followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    #关注
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    #取消关注
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    #查询去检查两个用户是否已关注
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    # 已关注用户的帖子查询
    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    # check_password()用先前生成的密码哈希值和用户在登录时输入的密码

    def check_password(self,password):
        return  check_password_hash(self.password_hash, password)

    #@login.user_loader装饰器 想flask-login注册用户加载函数，flask-login传递给函数的id作为一个参数，参数就是数据库主键
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))






class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(180))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}' .format(self.body)