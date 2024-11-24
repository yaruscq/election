# extensions.py


from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

login_manager = LoginManager()

bcrypt = Bcrypt()

mail = Mail()