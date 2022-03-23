
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



