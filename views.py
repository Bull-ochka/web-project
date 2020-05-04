from flask import render_template, redirect, request, url_for, jsonify
from flask_login import current_user
from models import *
from forms import *
from app import app

@app.route('/', methods=['GET'])
def index():
    boards = Board.query.all()
    return render_template('index.html', boards=boards)

@app.route('/<string:board_prefix>/', methods=['GET', 'POST'])
def board(board_prefix):
    form = NewThreadForm()

    if form.validate_on_submit():
        new_thread = Thread(title=form.title.data, board_prefix=board_prefix)
        db.session.add(new_thread)
        db.session.commit()
        new_post = Post(message=form.message.data, thread_id=new_thread.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('thread', board_prefix=board_prefix, thread_id=new_thread.id))

    board = Board.query.filter(Board.prefix == board_prefix).first_or_404()
    boards = Board.query.all()
    return render_template('board.html', board=board, form=form, boards=boards)

@app.route('/<string:board_prefix>/<int:thread_id>/', methods=['GET', 'POST'])
def thread(board_prefix, thread_id):
    form = NewPostForm()

    if form.validate_on_submit():
        new_post = Post(message=form.message.data, thread_id=thread_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('thread', board_prefix=board_prefix, thread_id=thread_id))

    board = Board.query.filter(Board.prefix == board_prefix).first_or_404()
    thread = board.threads.filter(Thread.id == thread_id).first_or_404()
    boards = Board.query.all()
    return render_template('thread.html', thread=thread, form=form, boards=boards)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
