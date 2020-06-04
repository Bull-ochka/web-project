from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)
db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# routes
from views import *
from api import api
from login import auth
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)

@login_manager.request_loader
def load_user_from_request(request):
    token = request.args.get('token')
    if token is None:
        token = request.headers.get('Authorization')
        if token is None:
            token = request.cookies.get('token')
            if token is None:
                return None

    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'))
        user = User.query.get(payload['id'])
        if user is not None and user.login_token == token:
            return user
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass

    return None
