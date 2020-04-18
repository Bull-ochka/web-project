from flask import render_template, redirect, request, url_for, jsonify
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


# REST API
@app.route('/api/board', methods=['GET'])
def api_board_all():
    boards = Board.query.all()
    return jsonify([x.serialize for x in boards])

@app.route('/api/board/<string:board_prefix>/', methods=['GET', 'POST'])
def api_board(board_prefix):
    # Must return not HTML page
    board = Board.query.filter(Board.prefix == board_prefix).first_or_404()
    threads = board.threads

    if request.method == 'POST':
        print(request.data)
        new_thread = Thread(title=request.json['title'], message=request.json['message'], board_prefix=board_prefix)
        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('thread', board_prefix=board_prefix, thread_id=new_thread.id))

    return jsonify([x.serialize for x in threads])

@app.route('/api/board/<string:board_prefix>/thread/<int:thread_id>', methods=['GET', 'POST'])
def api_thread(board_prefix, thread_id):
    # Must return not HTML page
    board = Board.query.filter(Board.prefix == board_prefix).first_or_404()
    thread = board.threads.filter(Thread.id == thread_id).first_or_404()

    if request.method == 'POST':
        new_post = Post(message=request.json['message'], thread_id=thread_id)
        db.session.add(new_post)
        db.session.commit()

    posts = thread.posts

    return jsonify([x.serialize for x in posts])
