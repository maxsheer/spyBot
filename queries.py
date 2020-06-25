CHECK_PLAYER_0 = "select * from Players where user_id='{id}'"
ADD_PLAYER_0 = "insert into Players (user_id, stage) values ('{id}', 0)"
UPDATE_STAGE_0 = "update Players set stage = {new_stage} where user_id = '{user_id}'"
CREATE_GAME_1 = "insert into Games (game_id, game_host, game_password, connected) values ('{game_id}', " \
                "'{host}', '{passwd}', 1)"
UPD_HOST_1 = "update Players set current_game_id = '{game_id}', connected = 1, stage = {new_stage} " \
             "where user_id='{user_id}'"
EXTRACT_GAME_ID_2 = "select current_game_id from Players where user_id='{user_id}'"
DELETE_GAME_2 = "delete from Games where game_id='{game_id}'"
UPD_PLAYERS_2 = "update Players set current_game_id = DEFAULT, connected = DEFAULT, stage = 0 where " \
                "current_game_id = '{game_id}'"
