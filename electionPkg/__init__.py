# __init__.py

import os
from flask import Flask
from .routes import main


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'

    from .models import db, User
    db.init_app(app)

    
    app.register_blueprint(main)

    from .extensions import bcrypt, login_manager
    login_manager.login_view = 'main.register'
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app