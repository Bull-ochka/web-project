from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from models import *
from forms import LoginForm
from config import SECRET_KEY
import jwt

auth = Blueprint('auth', __name__)


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
            return redirect(url_for('auth.login'))

        token = jwt.encode({
            'id': user.id,
            'create_time': datetime.utcnow().timestamp()
        }, SECRET_KEY, algorithm='HS256').decode()
        user.login_token = token
        db.session.commit()

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('token', token)
        return resp

    return render_template('login.html', form=form)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    pass

@auth.route('/logout/', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        current_user.login_token = None

    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('token')
    return resp
