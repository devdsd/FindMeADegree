import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_admin import Admin
# from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zqgm8FFVt5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/advisemedb'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

from app import routes
from app import engn3
