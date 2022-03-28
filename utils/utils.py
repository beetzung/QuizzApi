import json
import random
import string

QUESTIONS_NUMBER = 3


# generate token
def generate_random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


# save data as json
def save_data(data, name):
    with open(f'games/{name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


# read data from json
def read_data(name):
    with open(f'games/{name}.json') as json_file:
        data = json.load(json_file)
    return data


# check if file exists
def check_file(name):
    try:
        with open(f'games/{name}.json'):
            return True
    except FileNotFoundError:
        return False


# gets question ids from json
def get_question_ids():
    with open('../questions/quizz.json', encoding="utf8") as json_file:
        data = json.load(json_file)
        return random.sample(data.keys(), QUESTIONS_NUMBER)


# gets question from json
def get_question(q_id):
    # read json file
    with open('../questions/quizz.json') as json_file:
        data = json.load(json_file)
    return data[q_id]
