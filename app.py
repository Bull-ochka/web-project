from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from views import *
