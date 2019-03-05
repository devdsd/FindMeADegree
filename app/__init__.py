import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '7GM8fEHFdCnkb6n2mm'
app.config['DATABASE_URI'] = 'mysql://root:root@localhost/adviseme'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from app import routes