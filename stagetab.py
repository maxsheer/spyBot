handlers = ('spyBotprod_initial', 'spyBotprod_creategame', 'spyBotprod_hostgame',
            'spyBotprod_findgame_id', 'spyBotprod_findgamepass',
            'spyBotprod_deletegame', 'spyBotprod_gameparticipant')
payloads = {
    "zero":
        {
            "creategame": {
                "next_stage": 1,
                "keyboard": "back_only",
                "msg": "creategame_sendpass"
            },
            "findgame": {
                "next_stage": 4,
                "keyboard": "back_only",
                "msg": "findgame_sendid"
            }
        },
    "first":
        {
            "back": {
                "next_stage": 0,
                "keyboard": "initial",
                "msg": "mainmenu"
            },
        },
    "second":
        {
            "startgame": {
                "next_stage": 0,
                "keyboard": "initial",
                "msg": "startgame"
            },
            "delgame":
            {
                "next_stage": 0,
                "keyboard": "initial",
                "msg": "delgame"
            }
        },
    "fourth":
        {
            "back": {
                "next_stage": 0,
                "keyboard": "initial",
                "msg": "mainmenu"
            }
        }
}


# 0: initial. show main menu
# 1: creategame
# 2: hostgame
# 3: findgame
# 4: findgameid
# 5: findgamepass
# 6: deletegame
# 7: gameparticipant
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#