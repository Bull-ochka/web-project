from app import db


class Board(db.Model):
    prefix = db.Column(db.String(8), index=True, unique=True, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Board %r>' % self.name


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)

    def __repr__(self):
        return '<Thread %r>' % self.title


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2048))

    def __repr__(self):
        return '<Post %r>' % self.id
