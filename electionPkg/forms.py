from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('姓名：',
                           validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('電子信箱：',
                        validators=[DataRequired(), Email()])
    password = PasswordField('「邀請碼」：', validators=[DataRequired()])
    confirm_password = PasswordField('再次輸入「邀請碼」：',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('姓名：',
                           validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('電子信箱：',
                        validators=[DataRequired(), Email()])
    password = PasswordField('「投票密碼」', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')