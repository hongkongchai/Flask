#!/usr/bin/env python # -*- coding:utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from  flask_migrate import Migrate
app = Flask(__name__)
print('哪个包或模块在使用main函数',__name__)
app.config.from_object(Config)
print('秘钥',app.config['SECRET_KEY'])

db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app, db)#迁移引擎对象

from app import routes, models






