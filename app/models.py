#!/usr/bin/env python # -*- coding:utf-8 -*-

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


        #check_password()用先前生成的密码哈希值和用户在登录时输入的密码
    def check_password(self,password):
        return  check_password_hash(self.password_hash,password)

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