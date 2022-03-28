from game_core.player import Player, load_players_from_dict, save_players_to_dict
from game_core.question import load_question_from_dict

STATUS_CREATED = 'created'
STATUS_STARTED = 'started'
STATUS_FINISHED = 'finished'


class Game:
    def __init__(self, name: str, max_players: int, admin: str, version: str, question_ids: list,
                 players: dict = None,
                 status=STATUS_CREATED, admin_name=None, admin_token=None):
        self.name = name
        self.max_players = max_players
        self.admin = admin
        if players is not None:
            self.players = players
        else:
            self.players = {admin_token: Player(admin_name, admin_token)}
        self.status = status
        self.version = version
        self.question_ids = question_ids
        self.check_game()

    def is_created(self):
        return self.status == STATUS_CREATED

    def is_started(self):
        return self.status == STATUS_STARTED

    def is_finished(self):
        return self.status == STATUS_FINISHED

    def check_available_players(self):
        return len(self.players) < self.max_players

    def check_admin(self, token: str):
        return token == self.admin

    def check_user(self, token: str):
        return token in self.players

    def check_remaining_questions(self, token: str):
        player = self.players[token]
        return player.current_question < len(self.question_ids)

    def get_status(self):
        return self.status

    def get_player_name(self, token: str):
        return self.players[token].name

    def get_winner(self):
        return "TODO"

    def get_scoretable(self):
        table = []
        for player in self.players.values():
            table.append({
                'name': player.name,
                'score': player.score
            })
        return table

    def get_question_dict(self, token: str, func):
        if not self.check_remaining_questions(token):
            return None
        question = load_question_from_dict(func(self.get_next_question_id(token)))
        answers = []
        for answer in question.options.values():
            answers.append(answer)
        return {'text': question.text, 'answers': answers}

    def get_player_names(self):
        return [player.name for player in self.players.values()]

    def get_player_by_token(self, token: str):
        return self.players[token]

    def get_next_question_id(self, token: str):
        player = self.players[token]
        return self.question_ids[player.current_question]

    def check_game(self):
        all_finished = True
        for player in self.players.values():
            if player.current_question != len(self.question_ids):
                all_finished = False
                break
        if all_finished:
            self.finish()

    def add_player(self, name: str, token: str):
        if self.check_available_players():
            self.players[token] = Player(name, token)
            return True
        return False

    def begin(self):
        self.status = STATUS_STARTED

    def answer_question(self, token: str, answer: int, func):
        player = self.players[token]
        question = load_question_from_dict(func(self.get_next_question_id(token)))
        player.current_question += 1
        if question.check_answer(answer + 1):
            player.score += question.score
            result = True
        else:
            result = False
        self.check_game()
        return result

    def finish(self):
        self.status = STATUS_FINISHED

    def to_dict(self):
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
