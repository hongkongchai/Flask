#!/usr/bin/env python # -*- coding:utf-8 -*-
from flask import Flask
app = Flask(__name__)
print('哪个包或模块在使用main函数',__name__)

from app import routes






