#!/usr/bin/env python # -*- coding:utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from  flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)
#初始化Flask-login
login = LoginManager(app)
#要求用户登录
login.login_view = 'login'

app.config.from_object(Config)

db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app, db)#迁移引擎对象


from app import routes, models






