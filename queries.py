CHECK_PLAYER_0 = "select * from Players where user_id='{id}'"
ADD_PLAYER_0 = "insert into Players (user_id, stage) values ('{id}', 0)"
UPDATE_STAGE_0 = "update Players set stage = {new_stage} where user_id = '{user_id}'"
CREATE_GAME_1 = "insert into Games (game_id, game_host, game_password, connected) values ('{game_id}', " \
                "'{host}', '{passwd}', 1)"
UPD_HOST_1 = "update Players set current_game_id = '{game_id}', connected = 1, stage = {new_stage} " \
             "where user_id='{user_id}'"
EXTRACT_GAME_ID_2 = "select current_game_id from Players where user_id='{user_id}'"
DELETE_GAME_2 = "delete from Games where game_id='{game_id}'"
UPD_PLAYERS_2 = "update Players set stage = 0 where " \
                "current_game_id = '{game_id}'"
SEARCH_ID_3 = "select * from Games where game_id='{game_id}'"
UPDATE_PLAYERS_3 = "update Players set current_game_id = '{game_id}', connected = 0, " \
    "stage = {new_stage} where user_id = '{user_id}'"
CHECK_PASS_4 = "select game_password from Games where game_id = '{game_id}'"
PLAYER_ADD_4 = "update Players set connected = 1, stage = 6 where user_id = '{user_id}'"
UPDATE_GAME_4 = "update Games set connected = connected + 1 where game_id = '{game_id}'"
PLAYER_BACK_4 = "update Players set current_game_id = DEFAULT, connected = DEFAULT, stage = {new_stage}" \
    " where user_id='{user_id}'"
GET_TUPLE_SG = "select user_id from Players where current_game_id = '{game_id}' and connected = 1"
GET_E_TUPLE_SG = "select user_id from Players where current_game_id = '{game_id}'"
UPDATE_PLAYERS_SG = "update Players set connected = DEFAULT, current_game_id = DEFAULT, stage = 0 where current_game_id = '{game_id}'"
GET_HOST = "select game_host from Games where game_id = '{game_id}'"