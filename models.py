from datetime import datetime
from app import db


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

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'message'       : self.message,
            'datetime'      : self.datetime
        }

    def __repr__(self):
        return '<Post {} in {}>'.format(self.id, self.thread)
