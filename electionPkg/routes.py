# routes.py

from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .models import db, User, Candidates
from .extensions import login_manager, mail
from flask_login import login_user, logout_user, login_required, current_user, AnonymousUserMixin
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

您的「投票密碼是」：{ pwd_vote }</span>

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

    # Ensure the user is authenticated
    if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
        flash("您必需登入！", "warning")
        return redirect(url_for('main.login'))
    
    if current_user.voted:
        return render_template('logout.html', message="您已經投過票了！")
        return redirect(url_for('main.register'))

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
    else:
        flash('您投過了!!!', 'danger')
    # Handle form submission
    if request.method == 'POST':  # Check if it's a POST request
        
        
        
        if form.validate_on_submit():
            return redirect(url_for('main.vote'))
        else:
            flash('「投票密碼」不正確，請確認姓名、電子信箱和投票密碼是否正確!!!', 'danger')
    
    return render_template('login.html', title='Login', form=form)



@main.route('/qq_reset', methods=['POST', 'GET'])
def qq_reset():


    if request.method == 'GET':

        qq = User.query.filter_by(username='qq').first()
        qq.voted = False
        db.session.commit()
        flash('QQ 重置完成！')

    return redirect(url_for('main.register'))



@main.route('/tata_reset', methods=['POST', 'GET'])
def tata_reset():
    if request.method == 'GET':

        tata = User.query.filter_by(username='tata').first()
        tata.voted = False
        db.session.commit()
        flash('Tata 重置完成！')

    return redirect(url_for('main.register'))



@main.route('/others_reset', methods=['POST', 'GET'])
def others_reset():
    if request.method == 'GET':

        counterUser = User.query.count()
        print (type(counterUser))
        print(str(counterUser))
        
        if counterUser > 0:
            for x in range(counterUser):
            
                user = User.query.filter_by(id=x+1).first()
                if user:
                    user.voted = False
                    db.session.commit()
                    
    flash('測試員重置完成！')
    
    return redirect(url_for('main.register'))
    


@main.route('/result_reset', methods=['POST', 'GET'])
def result_reset():
    if request.method == 'GET':

        count_candidate = Candidates.query.count()
        print (type(count_candidate))
        print(str(count_candidate))
        
        if count_candidate > 0:
            for x in range(count_candidate):
            
                candidate = Candidates.query.filter_by(id=x+1).first()
                if candidate:
                    candidate.counter = 0
                    db.session.commit()
                    
    print('\n選票結果重置完成\n')
    return '<h1 class="margin-top:20px;">選票結果重置完成</h1>'
    




@main.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response