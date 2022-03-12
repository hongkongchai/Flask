#!/usr/bin/env python # -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, SubmitField


#注册
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码',validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


#登录
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me =BooleanField('记住我')
    submit = SubmitField('登录')


#编辑个人资料
class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('修改')

    #验证用户名
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('请使用不同的用户名.')

class PostForm(FlaskForm):
    post = TextAreaField('说点什么', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('提交')


