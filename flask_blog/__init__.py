import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '94c2ffd5f48a162262c4b3aa40d801b7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

from flask_blog.users.routes import users
from flask_blog.categories.routes import categories
from flask_blog.products.routes import products
from flask_blog.shipper.routes import shipper
from flask_blog.shippings.routes import shippings
from flask_blog.shops.routes import shops

app.register_blueprint(users)
app.register_blueprint(categories)
app.register_blueprint(products)
app.register_blueprint(shipper)
app.register_blueprint(shippings)
app.register_blueprint(shops)
