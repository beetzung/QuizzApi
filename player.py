import json


class Player:
    def __init__(self, name: str, token: str, admin=False, score=0):
        self.name = name
        self.is_admin = admin
        self.score = score
        self.token = token

    def to_dict(self):
        return {
            "name": self.name,
            "is_admin": self.is_admin,
            "score": self.score,
            "token": self.token
        }


def load_player_from_dict(d) -> Player:
    return Player(d["name"], d["token"], d["is_admin"], d["score"])


def load_players_from_dict(players_dict: dict) -> dict:
    players = {}
    for player_dict in players_dict.values():
        player = load_player_from_dict(player_dict)
        players[player.token] = player
    return players


def save_players_to_dict(players: dict) -> dict:
    players_dict = {}
    for player in players.values():
        players_dict[player.token] = player.to_dict()
    return players_dict
