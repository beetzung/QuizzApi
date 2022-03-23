
# QuizGame API

## Создать новую комнату
> https://quiz.beetzung.com/create?name={name}&players={players}


**name** - Имя игрока
**players** - максимум игроков

Пример ответа:

    {
      "data": {
        "password": "pbjtpw3fNO87ShSR3JBB8MMIn8L1yDmU",
        "token": "6AAmze5dUuDpVPAEuSRpu5oJgEUgyISa"
      }
    }

password - пароль для подключения
token - токен игрока

## Присоединиться к комнате
> https://quiz.beetzung.com/join?name={name}&password={password}

**name** - Имя игрока
**password** - пароль комнаты

Пример ответа:

    {
      "data": {
        "token": "pbjtpw3fNO87ShSR3JBB8MMIn8L1yDmU"
      }
    }

token - токен игрока

## Начать игру 
> https://quiz.beetzung.com/start?token={token}&password={password}

**token** - Токен админа
**password** - пароль комнаты

Пример ответа:

    {
      "status": "started"
    }

## Проверить игру
> https://quiz.beetzung.com/game?token={token}&password={password}

**token** - Токен админа
**password** - пароль комнаты

Пример ответа:

```
{
  "data": {
    "players": [
      "Anton",
      "test"
    ],
    "question": {
      "answers": {
        "1": "1909",
        "2": "1914",
        "3": "1919"
      },
      "text": "В каком году началась первая мировая война?"
    },
    "score": [
      [
        "Anton",
        0
      ],
      [
        "test",
        0
      ]
    ],
    "winner": "TODO"
  },
  "error": null,
  "status": "started"
}
```
question может быть Null если все вопросы отвечены

