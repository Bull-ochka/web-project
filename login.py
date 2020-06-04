from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from models import *
from forms import LogRegForm
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
    form = LogRegForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))

        if user.login_token is None:
            token = jwt.encode({
                'id': user.id,
                'create_time': datetime.utcnow().timestamp()
            }, SECRET_KEY, algorithm='HS256').decode()
            user.login_token = token
            db.session.commit()
        else:
            token = user.login_token

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('token', token)
        return resp

    return render_template('login.html', form=form)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = LogRegForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username is None:
            return jsonify(error.wrong_argument('username'))
        if password is None:
            return jsonify(error.wrong_argument('password'))

        user = User.query.filter(User.username == username).first()
        if user is not None:
            return redirect(url_for('auth.register'))

        if current_user.is_authenticated:
            current_user.login_token = None
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({
            'id': user.id,
            'create_time': datetime.utcnow().timestamp()
        }, SECRET_KEY, algorithm='HS256').decode()
        user.login_token = token
        db.session.commit()

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('token', token)
        return resp

    return render_template('register.html', form=form)

@auth.route('/logout/', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        current_user.login_token = None

    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('token')
    return resp
