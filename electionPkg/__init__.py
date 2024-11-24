# __init__.py

import os
from flask import Flask
from .routes import main


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')

    from .models import db, User
    db.init_app(app)

    from .errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    from .extensions import bcrypt, login_manager, mail
    login_manager.login_view = 'main.register'
    login_manager.login_message = "您得再次登入才能進入頁面！"  # Set a custom message
    login_manager.login_message_category = "warning"  # Optional: Bootstrap alert category
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)



    return app