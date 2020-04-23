from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)
db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# routes
from api import api
app.register_blueprint(api, url_prefix='/api')
from views import *

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))
