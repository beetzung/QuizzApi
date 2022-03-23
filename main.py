from flask import Flask, request, jsonify
from markupsafe import escape

from game_core import Game, load_game_from_dict
from player import Player
from utils import generate_random_token, save_data, read_data, check_file, get_question_ids

SUBDOMAIN = 'game'
VERSION = '1.0'
app = Flask(__name__)


@app.route('/create')  # , subdomain=SUBDOMAIN)
def create():
    players = int(escape(request.args.get('players')))
    name = escape(request.args.get('name'))
    password = generate_random_token()
    token = generate_random_token()
    admin = Player(name, token)
    game = Game(password, players, token, VERSION, get_question_ids(), {token: admin})
    save_data(game.to_dict(), password)
    return make_response(status_="created", data={'token': token, 'password': password})


@app.route('/join')  # , subdomain=SUBDOMAIN)
def join():
    password = escape(request.args.get('password'))
    name = escape(request.args.get('name'))
    if check_file(password):
        pass
    else:
        return make_response(error='No such game')
    game = load_game_from_dict(read_data(password))

    if game.is_created():
        if game.check_available_players():
            token = generate_random_token()
            game.add_player(name, token)
            save_data(game.to_dict(), password)
            return make_response(status_='joined', data={'token': token})
        else:
            return make_response(error='room is full')
    else:
        return make_response(error='Game already started or finished')


@app.route('/start')  # , subdomain=SUBDOMAIN)
def begin():
    password = escape(request.args.get('password'))
    token = escape(request.args.get('token'))
    if check_file(password):
        pass
    else:
        return make_response(error='No such game')
    data = read_data(password)
    game = load_game_from_dict(data)
    if not game.is_created():
        return make_response(error='Game already started or finished')
    if game.check_admin(token):
        game.begin()
        save_data(game.to_dict(), password)
        return make_response(status_='started')
    else:
        return make_response(error='Not admin')


@app.route('/game')  # , subdomain=SUBDOMAIN)
def status():
    password = escape(request.args.get('password'))
    token = escape(request.args.get('token'))
    if check_file(password):
        pass
    else:
        return make_response(error='No such game')
    data = read_data(password)
    game = load_game_from_dict(data)
    if not game.check_user(token):
        return make_response(error='Access denied')
    if game.is_created():
        return make_response(status_='created', data={
            'players': game.get_player_names()
        })
    elif game.is_finished():
        return make_response(status_='finished', data={
            'players': game.get_player_names(),
            'winner': game.get_winner(),
            'score': game.get_scoretable()
        })
    elif game.is_started():
        return make_response(status_='started', data={
            'question': 'TODO',
            'players': game.get_scoretable()
        })


def make_response(status_=None, error=None, data=None):
    return jsonify({'status': status_, 'error': error, 'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
