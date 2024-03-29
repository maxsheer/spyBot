keyboards = {
    "initial":
    {
      "one_time": False,
      "buttons": [
        [
          {
            "action": {
              "type": "text",
              "label": "Создать игру",
              "payload": "{\"info\": \"creategame\"}"
            },
            "color": "primary"
          }
        ],
        [
          {
            "action": {
              "type": "text",
              "label": "Найти игру",
              "payload": "{\"info\": \"findgame\"}"
            },
            "color": "primary"
          }
        ]
      ]
    },
    "back_only":
    {
      "one_time": False,
      "buttons": [
        [
          {
            "action": {
              "type": "text",
              "label": "Назад",
              "payload": "{\"info\": \"back\"}"
            },
            "color": "negative"
          }
        ]
      ]
    },
    "game_host":
    {
      "one_time": False,
      "buttons": [
        [
          {
            "action": {
              "type": "text",
              "label": "Начать игру",
              "payload": "{\"info\": \"startgame\"}"
            },
            "color": "primary"
          }
        ],
        [
          {
            "action": {
              "type": "text",
              "label": "Удалить игру",
              "payload": "{\"info\": \"delgame\"}"
            },
            "color": "negative"
          }
        ]
      ]
    },
    "game_participant":
    {
      "one_time": False,
      "buttons": [
        [
          {
            "action": {
              "type": "text",
              "label": "Выйти из игры",
              "payload": "{\"info\": \"exit_game\"}"
            },
            "color": "negative"
          }
        ]
      ]
    }
}

