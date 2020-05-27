from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

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

def create_app():
    pass
