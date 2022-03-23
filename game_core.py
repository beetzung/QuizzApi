from player import Player, load_players_from_dict, save_players_to_dict, load_player_from_dict

STATUS_CREATED = 'created'
STATUS_STARTED = 'started'
STATUS_FINISHED = 'finished'


class Game:
    def __init__(self, name: str, max_players: int, admin: str, version: str, question_ids: list,
                 players: dict = None,
                 status=STATUS_CREATED):
        self.name = name
        self.max_players = max_players
        self.admin = admin
        self.players = players
        self.status = status
        self.version = version
        self.question_ids = question_ids

    def is_created(self):
        return self.status == STATUS_CREATED

    def is_started(self):
        return self.status == STATUS_STARTED

    def is_finished(self):
        return self.status == STATUS_FINISHED

    def check_available_players(self):
        return len(self.players) < self.max_players

    def add_player(self, name: str, token: str):
        if self.check_available_players():
            self.players[token] = Player(name, token)
            return True
        return False

    def check_admin(self, token: str):
        return token == self.admin

    def check_user(self, token: str):
        return token in self.players

    def get_scoretable(self):
        return [(player.name, player.score) for player in self.players.values()]

    def get_winner(self):
        return max(self.players, key=lambda x: x.score)

    def begin(self):
        # TODO add questions
        self.status = STATUS_STARTED

    def to_dict(self):
        print(self.players)
        return {
            'name': self.name,
            'max_players': self.max_players,
            'admin': self.admin,
            'players': save_players_to_dict(self.players),
            'status': self.status,
            'version': self.version,
            'question_ids': self.question_ids
        }

    def __str__(self):
        return str(self.to_dict())


def load_game_from_dict(data: dict):
    return Game(
        name=data['name'],
        max_players=data['max_players'],
        admin=data['admin'],
        players=load_players_from_dict(data['players']),
        status=data['status'],
        version=data['version'],
        question_ids=data['question_ids']
    )
