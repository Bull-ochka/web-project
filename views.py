from flask import render_template, request
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<str:board_prefix>/', methods=['GET', 'POST'])
def board(board_prefix):
    if request.method == 'POST':
        # Здесь создаётся новый тред на выбранной борде
        pass
    else:
        return render_template('board.html')


@app.route('/<str:board_prefix>/<int:thread_id>/', methods=['GET', 'POST'])
def thread(board_prefix, thread_id):
    if request.method == 'POST':
        # Сюда приходит новый пост на выбранный тред
        pass
    else:
        return render_template('thread.html')


@app.errorhandler(404)
def not_found():
    return render_template('404.html'), 404
