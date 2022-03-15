import os
import click
from app import app


@app.cli.group()
def translate():
    # 翻译和本地化命令
    pass


@translate.command()
@click.argument('lang')
def init(lang):
    # 初始化一个新语言
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
