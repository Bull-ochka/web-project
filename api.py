from flask import Blueprint, request, url_for, jsonify, abort
from models import *

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
            'message': 'Argument "' + msg + '" is incorrect'
        }
    def wrong_url(msg):
        return {
            'status': 'error',
            'message': 'Path "' + msg + '" is wrong'
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
        new_post = Post(message=request.json['message'], thread_id=thread_id)
        db.session.add(new_post)
        db.session.commit()

        response['post_id'] = new_post.id
        return jsonify(response)

    last_id = request.args['last_id']
    # По факту сервер так и так ничего не отдаст, но грамотно говорить, где ошибка
    if not last_id.isdigit():
        return jsonify(error.wrong_argument('last_id'))
    posts = thread.posts.filter(Post.id > last_id).all()
    response['posts'] = list(map(lambda x: x.serialize, posts))

    return jsonify(response)

@api.route('/<path:path>')
def any_route(path):
    abort(404)

@api.errorhandler(404)
def not_found(e):
    return jsonify(error.wrong_url(request.path)), 404
