# routes.py

from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm

main = Blueprint('main', '__name__')

@main.route('/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if (form.username.data == 'qq' and form.email.data == 'qq@example.com') and form.password.data == '123':
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('投票「邀請碼」不正確，請確認姓名、電子信箱和邀請碼是否正確!!!', 'danger')

    return render_template('register.html', title="Register", form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.username.data == 'qq' and form.email.data == 'qq@example.com') and form.password.data == '456':
            flash('您可以投票了！', 'success')
            return redirect(url_for('main.vote'))
        else:
            flash('「投票密碼」不正確，請確認姓名、電子信箱和投票密碼是否正確!!!', 'danger')
    return render_template('login.html', title='Login', form=form)



@main.route('/vote')
def vote():
    message = '投票頁面'
    return render_template('vote.html', message=message)