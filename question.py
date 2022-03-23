class Question:
    def __init__(self, text: str, answer: int, category: str, score: int, options: dict):
        self.text = text
        self.answer = answer
        self.category = category
        self.score = score
        self.options = options

    def check_answer(self, answer: int) -> bool:
        return self.answer == answer

    def get_correct_answer(self):
        return self.options[str(self.answer)]

    def get_answer_options(self):
        return self.options.values()

    def to_dict(self):
        return {
            'text': self.text,
            'answer': self.answer,
            'category': self.category,
            'score': self.score,
            'options': self.options
        }


def from_dict(question_dict: dict) -> Question:
    return Question(
        question_dict['text'],
        question_dict['answer'],
        question_dict['category'],
        question_dict['score'],
        question_dict['options']
    )
