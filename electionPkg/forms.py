from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired


from .models import User
from .extensions import bcrypt


def check_registration_validate_credentials(form, field):
    """ username and pwd_invite checker"""

    username_entered = form.username.data
    # password_enter = form.password.data
    email_entered = form.email.data

    # check username is valid
    user_object = User.query.filter_by(username=username_entered).first()

    if user_object is None:
        raise ValidationError('名字或是電子信箱不正確！')
    elif email_entered != user_object.email:
    # elif not bcrypt.check_password_hash(user_object.password, password_enter):
        
        print(email_entered)
        raise ValidationError('名字或是電子信箱不正確！')
    


def check_login_validate_credentials(form, field):
    """ username and pwd_vote checker"""

    username_entered = form.username.data
    password_enter = form.password.data

    # check username is valid
    user_object = User.query.filter_by(username=username_entered).first()

    if user_object is None:
        raise ValidationError('名字或是投票密碼不正確！')
    elif password_enter != user_object.pwd_vote:
    # elif not bcrypt.check_password_hash(user_object.pwd_vote, password_enter):
        print(user_object.pwd_vote)
        print(password_enter)
        raise ValidationError('Password is incorrect!')
    


class RegistrationForm(FlaskForm):
    username = StringField('姓名：',
                           validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('電子信箱：',
                        validators=[DataRequired(), Email(), check_registration_validate_credentials])
    # email = StringField('電子信箱：', validators=[InputRequired(message='Password required'), check_registration_validate_credentials])
    # password = PasswordField('「邀請碼」：', validators=[InputRequired(message='Password required'), check_registration_validate_credentials])
    # confirm_password = PasswordField('再次輸入「邀請碼」：',
    #                                  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('姓名：',
                           validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('電子信箱：',
                        validators=[DataRequired(), Email()])
    password = PasswordField('「投票邀請碼」：', [InputRequired(message='Password required'), check_login_validate_credentials])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('開始投票')