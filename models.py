from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Board(db.Model):
    prefix = db.Column(db.String(8), index=True, unique=True, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    threads = db.relationship('Thread', backref='board', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'prefix'        : self.prefix,
            'name'          : self.name
        }

    def __repr__(self):
        return '<Board {}>'.format(self.name)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)

    board_prefix = db.Column(db.String(8), db.ForeignKey('board.prefix'), nullable=False)
    posts = db.relationship('Post', backref='thread', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'title'         : self.title
        }

    def __repr__(self):
        return '<Thread {} in {}>'.format(self.id, self.board)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'message'       : self.message,
            'datetime'      : self.datetime
        }

    def __repr__(self):
        return '<Post {} in {}>'.format(self.id, self.thread)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    threads = db.relationship('Thread', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.id)
