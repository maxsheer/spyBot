import requests
import json
import pymysql
import re
import datetime
import hashlib
import base64
import queries

print(queries.CHECK_PLAYER_0.format(
    id=str(123)
))
# conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678", "Spy", connect_timeout=5)
# cur = conn.cursor()
# cur.execute("select * from Players")
# resp = cur.fetchone()
# print(resp)
# conn.close()
# keyboard = {
#                 "one_time": False,
#                 "buttons": [
#                     [{
#                         "action": {
#                             "type": "text",
#                             "label": "Xyi",
#                             "payload": "stage.xyi"
#                         },
#                         "color": "blue"
#                     },
#                     {
#                         "action": {
#                             "type": "text",
#                             "label": "Pizda",
#                             "payload": "stage.pizda"
#                         },
#                         "color": "blue"
#                     }]
#                     ]
#             }
# str(keyboard)
# print(keyboard)
# params = {"a": "b", "c": "d", "keybpard": keyboard}
# params_lst = [f'{name}={value}' for name, value in params.items()]
# params = '&'.join(params_lst)
# print(params)

#api_url = "https://q3j3expx41.execute-api.us-east-1.amazonaws.com/version0/vkbot102515377298"

#r = requests.post(url=api_url)

#print(r)

#print('asd')
#print(r)

