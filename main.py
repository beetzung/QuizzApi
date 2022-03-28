import argparse
import json

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit
from markupsafe import escape

from game_core import Game, load_game_from_dict
from utils import generate_random_token, save_data, read_data, check_file, get_question_ids, get_question

HOST = "0.0.0.0"
PORT = 80
VERSION = '1.0'
app = Flask(__name__)
socket = SocketIO(app)


@socket.on('connect_to_game')
def connect(json_string):
    data = json.loads(json_string)
    password = escape(data['password'])
    token = escape(data['token'])
    if not check_file(password):
        get_response_dict(error='No such game')
        return
    game = load_game_from_dict(read_data(password))
    if not game.check_user(token):
        get_response_dict(error='Access denied')
        return
    join_room(password)
    print(f"Client {request.remote_addr} subscribed to {password}")


@socket.on('disconnect_from_game')
def disconnect(json_string):
    data = json.loads(json_string)
    password = escape(data('password'))
    leave_room(password)
    print(f"Client {request.remote_addr} unsubscribed from {password}")


@socket.on('request')
def request_question(json_string):
    data = json.loads(json_string)
    password = escape(data['password'])
    token = escape(data['token'])
    print(f"Client {request.remote_addr} requesting info for {password}")
    emit("game", get_response_dict(
        data=get_game_data(password),
        status_=get_game_status(password)
    ))
    emit("question", get_response_dict(status_=get_game_status(password), data=get_question_data(password, token)))


@socket.on('start')
def begin(json_string):
    data = json.loads(json_string)
    password = escape(data['password'])
    token = escape(data['token'])
    if check_file(password):
        pass
    else:
        emit("game", get_response_dict(error='No such game'))
    data = read_data(password)
    game = load_game_from_dict(data)
    if not game.is_created():
        emit("game", get_response_dict(error='Game already started or finished'))
    if game.check_admin(token):
        game.begin()
        save_data(game.to_dict(), password)
        print(f'Client {request.remote_addr} started game {password}')
        socket.emit("game", get_response_dict(
            data=get_game_data(password),
            status_=get_game_status(password)
        ), to=password)
        emit("question", get_response_dict(status_=get_game_status(password), data=get_question_data(password, token)))
    else:
        emit("game", get_response_dict(error='Access denied'))


@socket.on('answer')
def answer(json_string):
    data = json.loads(json_string)
    password = escape(data['password'])
    token = escape(data['token'])
    user_answer = data['answer']

    if check_file(password):
        pass
    else:
        emit("game", get_response_dict(error='No such game'))
    data = read_data(password)
    game = load_game_from_dict(data)
    if not game.check_user(token):
        emit("game", get_response_dict(error='Access denied'))
    if game.is_created():
        emit("game", get_response_dict(error='Game not finished'))
    elif game.is_finished():
        emit("game", get_response_dict(error='Game already finished'))
    elif game.is_started():
        if game.check_remaining_questions(token):
            if game.answer_question(token, user_answer, get_question):
                answered_correctly = True
            else:
                answered_correctly = False
            save_data(game.to_dict(), password)
            print(f"Client {request.remote_addr} answered question for {password}, answer={user_answer}")
            response = get_response_dict(
                status_=game.get_status(),
                data=get_question_data(password, token, answer_status=answered_correctly)
            )
            emit("question", response)
            socket.emit("game", get_response_dict(game.get_status(), data=get_game_data(password)), to=password)
        else:
            emit("game", get_response_dict(error='No more questions'))


@socket.on('connect')
def test_connect(auth):
    print(f"Client {request.remote_addr} connected with auth {auth}")


@socket.on('disconnect')
def test_disconnect():
    print(f"Client {request.remote_addr} disconnected")


@app.route('/create')
def create():
    players = int(escape(request.args.get('players')))
    name = escape(request.args.get('name'))
    password = generate_random_token()
    token = generate_random_token()
    game = Game(password, players, token, VERSION, get_question_ids(), admin_name=name, admin_token=token)
    save_data(game.to_dict(), password)
    print(f"Client {request.remote_addr} created game {password}")
    return jsonify(get_response_dict(status_="created", data={'token': token, 'password': password}))


@app.route('/join')
def join():
    password = escape(request.args.get('password'))
    name = escape(request.args.get('name'))
    if check_file(password):
        pass
    else:
        return jsonify(get_response_dict(error='No such game'))
    game = load_game_from_dict(read_data(password))

    if game.is_created():
        if game.check_available_players():
            token = generate_random_token()
            game.add_player(name, token)
            save_data(game.to_dict(), password)
            print(f"Client {request.remote_addr} joined game {password}")
            return jsonify(get_response_dict(status_='joined', data={'token': token}))
        else:
            return jsonify(get_response_dict(error='room is full'))
    else:
        return jsonify(get_response_dict(error='Game already started or finished'))


def get_game_data(password):
    game = load_game_from_dict(read_data(password))
    return {
        'players': game.get_player_names(),
        'winner': game.get_winner(),
        'score': game.get_scoretable()
    }


def get_game_status(password):
    game = load_game_from_dict(read_data(password))
    return game.get_status()


def get_question_data(password, token, answer_status=None):
    game = load_game_from_dict(read_data(password))
    data = {
        'name': game.get_player_name(token),
        'is_admin': game.check_admin(token),
        'question': game.get_question_dict(token, get_question),
        "answered_correctly": answer_status
    }
    print(data)
    return data


def get_response_dict(status_=None, data=None, error=None):
    d = {
        "status": status_,
        "data": data,
        "error": error
    }
    return d


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--production', action='store_true',
                        help='Run in production mode (must have SSL cert.pem and key.pem')
    args = parser.parse_args()
    if args.production:
        socket.run(app, host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
    else:
        socket.run(app, host='0.0.0.0', port=80)
