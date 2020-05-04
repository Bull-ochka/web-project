from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from models import *
from forms import LoginForm
from config import SECRET_KEY
import jwt

auth = Blueprint('login', __name__)


class error:
    def not_auth():
        return {
            'status': 'error',
            'message': 'User not auth'
        }


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user)

        resp = make_response(redirect(url_for('index')))
        token = jwt.encode({
            'id': user.id,
            'create_time': datetime.utcnow().timestamp()
        }, SECRET_KEY, algorithm='HS256')
        resp.set_cookie('token', token.decode())
        return resp

    return render_template('login.html', form=form)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    pass

@auth.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))
