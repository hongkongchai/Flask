#!/usr/bin/env python # -*- coding:utf-8 -*-
from flask import Flask
from config import Config
app = Flask(__name__)
print('哪个包或模块在使用main函数',__name__)
app.config.from_object(Config)
print('秘钥',app.config['SECRET_KEY'])

from app import routes






