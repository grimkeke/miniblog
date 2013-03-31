from sys import platform
from os import system

system('which python')
system('pip install flask')
system('pip install flask-login')
system('pip install flask-openid')
if platform == 'win32':
    system('pip install --no-deps lamson chardet flask-mail')
else:
    system('pip install flask-mail')
system('pip install sqlalchemy==0.7.9')
system('pip install flask-sqlalchemy')
system('pip install sqlalchemy-migrate')
system('pip install flask-whooshalchemy')
system('pip install flask-wtf')
system('pip install flask-babel')
system('pip install flup')
system('pip install guess-language')
