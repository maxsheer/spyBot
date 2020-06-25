import os
import json
from typing import (Any, Tuple, Optional)
import boto3
import vkbot
import keyboards
import pymysql
import queries
import messages
import stagetab


def get_player_info(user_id: str) -> Tuple:
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678", "Spy",
                           connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.CHECK_PLAYER_0.format(
        id=user_id
    ))
    out = cur.fetchone()
    conn.close()
    return out


def add_player(user_id: str) -> None:
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678", "Spy",
                           connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.ADD_PLAYER_0.format(
        id=user_id
    ))
    conn.commit()
    conn.close()


def handle_stage(pl_info: Tuple, event: dict) -> Any:

    client = boto3.client('lambda')
    resp = client.invoke(
        FunctionName=stagetab.handlers[pl_info[3]],
        InvocationType='Event',
        Payload=json.dumps(event)
    )
    return resp


def main(event: dict, context: Optional[Any] = None) -> dict:
    print(event)
    del context  # Unused
    vk_api_key = os.environ["VK_API_KEY"]
    vk_api_ver = os.environ["VK_API_VER"]
    try:
        if event['type'] == 'message_new':
            print('started')
        pl_info = get_player_info(event['object']['message']['from_id'])
        if pl_info:
            handle_stage(pl_info, event)
        else:
            add_player(str(event['object']['message']['from_id']))
            child = vkbot.VkBot(vk_api_key, vk_api_ver)
            keyboard = keyboards.keyboards['initial']
            msg = messages.messages['initial']
            print(child.send_message(str(event["object"]["message"]["from_id"]), msg, json.dumps(keyboard)).json())
    except KeyError:
        print("NoKey")
    except pymysql.Error:
        print("DbError")
    return {"code": "200",
            "data": "OK"}
