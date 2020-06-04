from flask import Blueprint, request, url_for, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from models import *
from config import SECRET_KEY
import jwt

api = Blueprint('api', __name__)


class error:
    def not_found(msg):
        return {
            'status': 'error',
            'message': msg + ' not found'
        }
    def wrong_argument(msg):
        return {
            'status': 'error',
            'message': 'Argument "' + msg + '" is incorrect or missing'
        }
    def wrong_url(msg):
        return {
            'status': 'error',
            'message': 'Path "' + msg + '" is wrong'
        }
    def wrong_login_data():
        return {
            'status': 'error',
            'message': 'Wrong username/password'
        }
    def wrong_format():
        return {
            'status': 'error',
            'message': 'Data has wrong format'
        }
    def no_permission():
        return {
            'status': 'error',
            'message': 'User hasn\'t enough permissions'
        }
    def username_busy():
        return {
            'status': 'error',
            'message': 'This username already taken'
        }
    def unauthorized():
        return {
            'status': 'error',
            'message': 'User must be authorized'
        }


@api.route('/board/', methods=['GET'])
def api_board_all():
    boards = Board.query.all()
    return jsonify([x.serialize for x in boards])

@api.route('/board/<string:board_prefix>/', methods=['GET', 'POST'])
def api_board(board_prefix):
    board = Board.query.filter(Board.prefix == board_prefix).first()
    if (board == None):
        return jsonify(error.not_found('Board'))

    response = {
        'status': 'ok'
    }

    if request.method == 'POST':
        title = request.json.get('title')
        message = request.json.get('message')

        if title is None:
            return jsonify(error.wrong_argument('title'))
        if message is None:
            return jsonify(error.wrong_argument('message'))

        new_thread = Thread(title=title, message=message, board_prefix=board_prefix)
        db.session.add(new_thread)
        db.session.commit()

        response['url'] = url_for('thread', board_prefix=board_prefix, thread_id=new_thread.id)

        return jsonify(response)

    # GET method
    last_id = request.args.get('last_id')
    if last_id is None:
        last_id = '0'
    # По факту сервер так и так ничего не отдаст, но грамотно говорить, где ошибка
    if not last_id.isdigit():
        return jsonify(error.wrong_argument('last_id'))
    threads = board.threads.filter(Thread.id > last_id).all()
    response['threads'] = list(map(lambda x: x.serialize, threads))

    return jsonify(response)

@api.route('/board/<string:board_prefix>/thread/<int:thread_id>/', methods=['GET', 'POST'])
def api_thread(board_prefix, thread_id):
    board = Board.query.filter(Board.prefix == board_prefix).first()
    if (board == None):
        return jsonify(error.not_found('Board'))

    thread = board.threads.filter(Thread.id == thread_id).first()
    if (thread == None):
        return jsonify(error.not_found('Thread'))

    response = {
        'status': 'ok'
    }

    if request.method == 'POST':
        user_id = None if not current_user.is_authenticated else current_user.id
        message = request.json.get('message')
        print(message)

        if message is None:
            return jsonify(error.wrong_argument('message'))

        new_post = Post(message=message, thread_id=thread_id, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        response['post_id'] = new_post.id
        return jsonify(response)

    last_time = request.args.get('last_time')
    if last_time is None:
        last_time = '0'
    # По факту сервер так и так ничего не отдаст, но грамотно говорить, где ошибка
    try:
        last_time = float(last_time)
    except:
        return jsonify(error.wrong_argument('last_time'))
    dt = datetime.fromtimestamp(last_time)
    posts = thread.posts.filter(Post.datetime > dt).all()

    def set_mine_flag(post):
        obj = post.serialize
        if current_user.is_authenticated:
            obj['mine'] = current_user.id == post.user_id
        else:
            obj['mine'] = False
        return obj

    response['posts'] = list(map(set_mine_flag, posts))

    return jsonify(response)

@api.route('/edit/post/<int:post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return jsonify(error.not_found('Post with id={}'.format(post_id)))
    if post.user_id != current_user.id:
        return jsonify(error.no_permission())

    response = {
        'status': 'ok'
    }

    message = request.json.get('message')
    if message is None:
        return jsonify(error.wrong_argument('message'))
    post.message = message
    post.datetime = datetime.utcnow()
    db.session.commit()

    return jsonify(response)

@api.route('/login/', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None:
        return jsonify(error.wrong_argument('username'))
    if password is None:
        return jsonify(error.wrong_argument('password'))

    user = User.query.filter(User.username == username).first()
    if user is None or not user.check_password(password):
        return jsonify(error.wrong_login_data())
    if user.login_token is None:
        token = jwt.encode({
            'id': user.id,
            'create_time': datetime.utcnow().timestamp()
        }, SECRET_KEY, algorithm='HS256').decode()
        user.login_token = token
        db.session.commit()
    else:
        token = user.login_token
    return jsonify({ 'status': 'ok', 'token': token })

@api.route('/register/', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None:
        return jsonify(error.wrong_argument('username'))
    if password is None:
        return jsonify(error.wrong_argument('password'))

    user = User.query.filter(User.username == username).first()
    if user is not None:
        return jsonify(error.username_busy())

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

    return jsonify({ 'status': 'ok', 'token': token })


@api.route('/logout/', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        current_user.login_token = None
    return jsonify({ 'status': 'ok' })

@api.route('/<path:path>')
def any_route(path):
    abort(404)

# UNAUTHORIZED
@api.errorhandler(401)
def unauthorized(e):
    return jsonify(error.unauthorized()), 401

# NOT FOUND
@api.errorhandler(404)
def not_found(e):
    return jsonify(error.wrong_url(request.path)), 404
