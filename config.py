#!/usr/bin/env python # -*- coding:utf-8 -*-
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'