#!/usr/bin/env python # -*- coding:utf-8 -*-
from app import app,db
from app.models import User,Post

@app.shell_context_processor
def mask_shell_context():
    #创建shell上下文，将数据库实例模型添加到shell会话中
    return {'db': db, 'User': User, 'Post': Post}

if __name__=='__main__':

    app.run(debug=True)
