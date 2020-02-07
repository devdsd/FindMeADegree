import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zqgm8FFVt5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/advisemedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app2 = Flask(__name__)
app2.config['SECRET_KEY'] = 'secretkey231'
app2.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/advisemedb'
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db2 = SQLAlchemy(app2)
login_manager2 = LoginManager(app2)
bcrypt2 = Bcrypt(app2)
login_manager2.login_view = 'login'
login_manager2.login_message_category = 'info'



from app import routes

from app import routes2

from app import engine
