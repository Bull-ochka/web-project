from flask import render_template, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user
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


# LOGIN
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('abc')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


# REST API
def error_not_found(msg):
    return {
        'status': 'error',
        'message': msg + ' not found'
    }
def error_wrong_argument(msg):
    return {
        'status': 'error',
        'message': 'Argument "' + msg + '" is incorrect'
    }

@app.route('/api/board/', methods=['GET'])
def api_board_all():
    boards = Board.query.all()
    return jsonify([x.serialize for x in boards])

@app.route('/api/board/<string:board_prefix>/', methods=['GET', 'POST'])
def api_board(board_prefix):
    board = Board.query.filter(Board.prefix == board_prefix).first()
    if (board == None):
        return jsonify(error_not_found('Board'))

    response = {
        'status': 'ok'
    }

    if request.method == 'POST':
        print(request.data)
        new_thread = Thread(title=request.json['title'], message=request.json['message'], board_prefix=board_prefix)
        db.session.add(new_thread)
        db.session.commit()

        response['url'] = url_for('thread', board_prefix=board_prefix, thread_id=new_thread.id)

        return jsonify(response)

    # GET method
    last_id = request.args['last_id']
    # По факту сервер так и так ничего не отдаст, но грамотно говорить, где ошибка
    if not last_id.isdigit():
        return jsonify(error_wrong_argument('last_id'))
    threads = board.threads.filter(Thread.id > last_id).all()
    response['threads'] = list(map(lambda x: x.serialize, threads))

    return jsonify(response)

@app.route('/api/board/<string:board_prefix>/thread/<int:thread_id>/', methods=['GET', 'POST'])
def api_thread(board_prefix, thread_id):
    board = Board.query.filter(Board.prefix == board_prefix).first()
    if (board == None):
        return jsonify(error_not_found('Board'))

    thread = board.threads.filter(Thread.id == thread_id).first()
    if (thread == None):
        return jsonify(error_not_found('Thread'))

    response = {
        'status': 'ok'
    }

    if request.method == 'POST':
        new_post = Post(message=request.json['message'], thread_id=thread_id)
        db.session.add(new_post)
        db.session.commit()

        response['post_id'] = new_post.id
        return jsonify(response)

    last_id = request.args['last_id']
    # По факту сервер так и так ничего не отдаст, но грамотно говорить, где ошибка
    if not last_id.isdigit():
        return jsonify(error_wrong_argument('last_id'))
    posts = thread.posts.filter(Post.id > last_id).all()
    response['posts'] = list(map(lambda x: x.serialize, posts))

    return jsonify(response)
