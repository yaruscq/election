# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Use pytz if on Python <3.9
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

db = SQLAlchemy()

class User(db.Model):
    """ User model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd_invite = db.Column(db.String(50), nullable=False)
    pwd_vote = db.Column(db.String(50), nullable=False)
    voted = db.Column(db.Boolean, default=False, nullable=False)
    time_voted = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Taipei')).replace(microsecond=0))

    def __repr__(self):
        return f'<User: {self.username} || Email: {self.email} || pwd_invite: {self.pwd_invite} || pwd_vote: {self.pwd_vote} || voted: {self.voted} || time_voted: {self.time_voted}>'
    
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True  # You can add more complex logic if needed

    def is_active(self):
        """Return True if the user account is active."""
        return self.active

    def is_anonymous(self):
        """Return False because this is not an anonymous user."""
        return False

    def get_id(self):
        # Flask-Login uses this to identify the user. Return pwd_invite instead of id or username.
        """Return the unique identifier for the user."""
        return self.username  # Or self.id if you prefer
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'username': self.pwd_invite})


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            pwd_invite = s.loads(token, max_age=1800)['pwd_invite']
        except:
            return None
        return User.query.get(pwd_invite)


class Candidates(db.Model):
    """ Candidates model """
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    counter = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<id: {self.id}> User: {self.name} || counter: {self.counter}>'