# routes.py

from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .models import db, User, Candidates
from .extensions import login_manager, mail
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message



main = Blueprint('main', '__name__')


# With "pwd_invite"
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


def send_pwd_vote_email(user_object):
    token = user_object.get_reset_token()
    pwd_vote=user_object.pwd_vote
    msg = Message('中華奧會運動員委員會選任委員投票網站邀請碼', sender='fedo.chou@gmail.com', recipients=[user_object.email])
    msg.body = f'''請登入下列網址，輸入您的「姓名」、「電子信箱」和下方的「投票邀請碼」後，進行投票:
{url_for('main.reset_token', token=token, _external=True)}

您的「投票密碼是」：{ pwd_vote }

提醒您，每人只有一次投票機會！
有任何疑問，請於上班時間來電：(02)8771-1387 陳小姐

'''
    mail.send(msg)


@main.route('/', methods=['POST', 'GET'])
def register():

    form = RegistrationForm()

    if request.method == 'POST':  # Check if it's a POST request
        if form.validate_on_submit():
            # if (form.username.data == 'qq' and form.email.data == 'qq@example.com') and form.password.data == '123':
            #     flash(f'Account created for {form.username.data}!', 'success')
            user_object = User.query.filter_by(username=form.username.data).first()
            # Todo: send mail
            flash(f'您的投票密碼已寄出，請到電子信箱查閱！{user_object.email}')

            login_user(user_object)
            print(f'\nValid user: {user_object.username}\n')
            send_pwd_vote_email(user_object)
            return redirect(url_for('main.login'))
        else:
            flash('請確認姓名或電子信箱是否正確!!!', 'danger')

    return render_template('register.html', title="Register", form=form)



@main.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    form = LoginForm()
    if current_user.voted == True:
            message='您已經投過票了！'
            flash('您投過了!!!', 'danger')
            return redirect(url_for('main.logout', message=message))
    # Handle form submission
    if request.method == 'POST':  # Check if it's a POST request
        
        
        
        if form.validate_on_submit():
            return redirect(url_for('main.vote'))
        else:
            flash('「投票密碼」不正確，請確認姓名、電子信箱和投票密碼是否正確!!!', 'danger')
    
    return render_template('login.html', title='Login', form=form)



@main.route('/vote', methods=['POST', 'GET'])
@login_required
# def vote():
#     message = '投票頁面'
#     candidates_count = Candidates.query.count()
#     print('candidates count = ' + str(candidates_count))

#     candidates = Candidates.query.all()

#     return render_template('vote.html', message=message, candidates=candidates)
def vote():

    if current_user.voted == True:
        return render_template('logout.html', message="您已經投過票了！")

    message = '投票頁面'
    candidates_limit = 5
    candidates_count = Candidates.query.count()
    print('candidates count = ' + str(candidates_count))

    candidates = Candidates.query.all()

    if request.method == 'POST':
        selected_candidates = request.form.getlist('candidates')
        
        if len(selected_candidates) > candidates_limit:
            flash(f"您最多只能選擇 {candidates_limit} 名候選人！", "error")
            return redirect(url_for('main.vote'))
        
        # Store the votes in the database
        for candidate_id in selected_candidates:
            candidate = Candidates.query.get(candidate_id)
            if candidate:
                candidate.counter += 1
        
        # Mark the user as having voted
        current_user.voted = True

        # Indicate when the user votes
        time_voted = datetime.now(ZoneInfo('Asia/Taipei')).replace(microsecond=0)
        current_user.time_voted = time_voted

        db.session.commit()
        print('username = ' + current_user.username)
        print(current_user.voted)
        logout_user()
        # todo: voter cannot vote, logout, change voted status 
        #       mail : send vote-ticket code
        #       Result route and admin 

        return redirect(url_for('main.logout'))
    
    # Retrieve candidates from the database
    candidates = Candidates.query.all()
    
    return render_template('vote.html', candidates=candidates, message=message)



@main.route('/logout')
def logout():
    logout_user()
    flash('完成投票！', 'info')
    # return redirect(url_for('main.logout'))
    return render_template('logout.html', message="恭喜，您已經完成投票！")


@main.route('/result')
def result():
    candidates = Candidates.query.order_by(Candidates.counter.desc()).all()
    return render_template('result.html', candidates=candidates)



@main.route('/login/<token>', methods=['GET', 'POST'])
def reset_token(token):
    form = LoginForm()
    if current_user.voted == True:
            message='您已經投過票了！'
            flash('您投過了!!!', 'danger')
            return redirect(url_for('main.logout', message=message))
    # Handle form submission
    if request.method == 'POST':  # Check if it's a POST request
        
        
        
        if form.validate_on_submit():
            return redirect(url_for('main.vote'))
        else:
            flash('「投票密碼」不正確，請確認姓名、電子信箱和投票密碼是否正確!!!', 'danger')
    
    return render_template('login.html', title='Login', form=form)