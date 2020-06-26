import requests
import datetime
import os
import json
import re
from typing import (Any, AnyStr, List, Tuple, Optional, Dict, Callable)
import boto3
import vkbot
import keyboards
import pymysql
import queries
import messages
import stagetab
import hashlib
import base64
import random
import locations

# ----------------------startgame-----------------------------------------


def get_gamehost(game_id):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.GET_HOST.format(
        game_id=game_id
    ))
    info = cur.fetchone()
    conn.close()
    return info


def spyBotprod_remindhost(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    game_id = event['game_id']
    try:
        child = vkbot.VkBot(vk_api_ver, vk_api_key)
        info = get_gamehost(game_id)[0]
        msg = messages.messages['remind_host'].format(num_con=info[1])
        print(child.send_message(info[0], msg).json())
    except KeyError as e:
        print("KE: " + e.__str__())
    except pymysql.Error as e:
        print("PME " + e.__str__())
    return {
        "STATUS": "OK"
    }


# ----------------------startgame-----------------------------------------


def get_entire_dg(game_id: str) -> Tuple[Tuple]:
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.GET_E_TUPLE_SG.format(
        game_id=game_id
    ))
    entire_tuple = cur.fetchall()
    cur.execute(queries.UPDATE_PLAYERS_SG.format(
        game_id=game_id
    ))
    conn.commit()
    conn.close()
    return entire_tuple


def spyBotprod_delgame(event: dict, context: Optional) -> dict:
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    game_id = event['game_id']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        entire_tuple = get_entire_dg(game_id)
        msg = 'Игра была удалена:('
        keyboard = keyboards.keyboards['initial']
        for i in entire_tuple:
            print(child.send_message(i[0], msg, json.dumps(keyboard)).json())
    except KeyError as e1:
        print("smth wrong " + e1.__str__())
    except pymysql.Error as e2:
        print("smth wrong with db" + e2.__str__())
    return {
        "status": "OK"
    }


# ----------------------startgame-----------------------------------------

def get_tuples(game_id: str):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.GET_TUPLE_SG.format(
        game_id=game_id
    ))
    user_tuple = cur.fetchall()
    cur.execute(queries.GET_E_TUPLE_SG.format(
        game_id=game_id
    ))
    entire_tuple = cur.fetchall()
    cur.execute(queries.UPDATE_PLAYERS_SG.format(
        game_id=game_id
    ))
    conn.commit()
    conn.close()
    return user_tuple, entire_tuple


def form_spy_msg() -> str:
    dm = '!!!!! ВЫ - ШПИОН !!!!!\n'
    dm1 = '\n'.join(locations.locations)
    return dm + 'СПИСОК ЛОКАЦИЙ:' + dm1 + dm


def spyBotprod_startgame(event: dict, context: Optional) -> dict:
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    game_id = event['game_id']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        users_tuple, entire_tuple = get_tuples(game_id)
        spy = random.choice(users_tuple)[0]
        location = random.choice(locations.locations)
        for i in users_tuple:
            if i[0] == spy:
                msg = form_spy_msg()
            else:
                msg = messages.messages['loc_msg'] + location
            print(child.send_message(i[0], msg))
        msg = messages.messages['game_started']
        keyboard = keyboards.keyboards['initial']
        for i in entire_tuple:
            print(child.send_message(i[0], msg, json.dumps(keyboard)).json())
    except KeyError as e:
        print("smth wrong with payload " + e.__str__())
    except pymysql.Error as e:
        print("smth wrong with dbase: " + e.__str__())
    return {
        "status": "OK"
    }


# ----------------------findgameid-----------------------------------------

def check_pw_3(pw: str) -> object:
    regex = re.compile('[^a-zA-Z0-9]')
    return regex.search(pw)


def remind_game_host(game_id):
    event = dict()
    event['game_id'] = game_id
    client = boto3.client('lambda')
    resp = client.invoke(
        FunctionName='spyBotprod_remindhost',
        InvocationType='Event',
        Payload=json.dumps(event)
    )
    return resp


def process_password_fg(event):
    pw = event['object']['message']['text']
    bad_pass = check_pw_3(pw)
    if not bad_pass:
        conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                               "Spy", connect_timeout=5)
        cur = conn.cursor()
        cur.execute(queries.EXTRACT_GAME_ID_2.format(
            user_id=event['object']['message']['from_id']
        ))
        game_id = cur.fetchone()[0]
        cur.execute(queries.CHECK_PASS_4.format(
            game_id=game_id
        ))
        game_pass = cur.fetchone()[0]
        if pw == game_pass:
            cur.execute(queries.PLAYER_ADD_4.format(
                user_id=event['object']['message']['from_id']
            ))
            cur.execute(queries.UPDATE_GAME_4.format(
                game_id=game_id
            ))
            conn.commit()
            print(remind_game_host(game_id))
            msg = messages.messages['succ_fg']
            keyboard = keyboards.keyboards['game_participant']
        else:
            msg = messages.messages['fail_fg']
            keyboard = keyboards.keyboards['back_only']
        conn.close()
    else:
        msg = messages.messages['failpass_gc']
        keyboard = keyboards.keyboards['back_only']
    return msg, keyboard


def process_payload_fourth(payload, event):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.PLAYER_BACK_4.format(
        new_stage=stagetab.payloads['fourth'][payload]['next_stage'],
        user_id=event['object']['message']['from_id']
    ))
    conn.commit()
    conn.close()
    msg = messages.messages[stagetab.payloads['fourth'][payload]['msg']]
    keyboard = keyboards.keyboards[stagetab.payloads['fourth'][payload]['keyboard']]
    return msg, keyboard


def spyBotprod_findgame_id(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg, keyboard = process_password_fg(event)
        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['fourth']:
                msg, keyboard = process_payload_fourth(payload, event)
            else:
                msg = messages.messages['payload_err']
                keyboard = keyboards.keyboards['back_only']
        print(child.send_message(str(event['object']['message']['from_id']),
                                 msg, json.dumps(keyboard)).json())
    except KeyError:
        print('smth wrong')
    except pymysql.Error:
        print('smth wrong w/ bd')
    return {
        "status": "OK"
    }


# ----------------------findgame-----------------------------------------


def check_id(pw: str) -> object:
    regex = re.compile('[^a-zA-Z0-9]')
    return regex.search(pw)


def process_id(event):
    prov_id = event['object']['message']['text']
    bad_id = check_id(prov_id)
    if not bad_id:
        conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                               "Spy", connect_timeout=5)
        cur = conn.cursor()
        cur.execute(queries.SEARCH_ID_3.format(
            game_id=prov_id
        ))
        if cur.fetchone():
            cur.execute(queries.UPDATE_PLAYERS_3.format(
                game_id=prov_id,
                new_stage=5,
                user_id=event['object']['message']['from_id']
            ))
            conn.commit()
            msg = messages.messages['goodid']
            keyboard = keyboards.keyboards['back_only']
        else:
            msg = messages.messages['badid']
            keyboard = keyboards.keyboards['back_only']
        conn.close()
    else:
        msg = messages.messages['failpass_gc']
        keyboard = keyboards.keyboards['back_only']
    return msg, keyboard


def process_payload_third(payload, event):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.UPDATE_STAGE_0.format(
        user_id=event['object']['message']['from_id'],
        new_stage=stagetab.payloads['third'][payload]['next_stage']
    ))
    conn.commit()
    conn.close()
    msg = messages.messages[stagetab.payloads['third'][payload]['msg']]
    keyboard = keyboards.keyboards[stagetab.payloads['third'][payload]['keyboard']]
    return msg, keyboard


def spyBotprod_findgame(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg, keyboard = process_id(event)
        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['third']:
                msg, keyboard = process_payload_third(payload, event)
            else:
                msg = messages.messages['payload_err']
                keyboard = keyboards.keyboards['back_only']
        print(child.send_message(str(event['object']['message']['from_id']),
                                 msg, json.dumps(keyboard)).json())
    except KeyError:
        print('smth wrong')
    except pymysql.Error:
        print('smth wrong w/ bd')
    return {
        "status": "OK"
    }


# ----------------------hostgame-----------------------------------------


def invoke_game_delstart(payload, game_id):
    fn = 'spyBotprod_delgame' if payload == 'delgame' else 'spyBotprod_startgame'
    client = boto3.client('lambda')
    event = dict()
    event['game_id'] = game_id 
    resp = client.invoke(
        FunctionName=fn,
        InvocationType='Event',
        Payload=json.dumps(event)
    )
    return resp


def process_payload_second(payload, event):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.EXTRACT_GAME_ID_2.format(
        user_id=event['object']['message']['from_id']
    ))
    game_id = cur.fetchone()[0]
    cur.execute(queries.UPD_PLAYERS_2.format(
        game_id=game_id
    ))
    conn.commit()
    conn.close()
    print(invoke_game_delstart(payload, game_id))
    msg = messages.messages[stagetab.payloads['second'][payload]['msg']]
    keyboard = keyboards.keyboards[stagetab.payloads['second'][payload]['keyboard']]
    return msg, keyboard


def spyBotprod_hostgame(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg = messages.messages['zero_error']
            keyboard = keyboards.keyboards['game_host']

        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['second']:
                msg, keyboard = process_payload_second(payload, event)
            else:
                msg = messages.messages['payload_err']
                keyboard = keyboards.keyboards['initial']
        print(child.send_message(str(event['object']['message']['from_id']),
                                 msg, keyboard))
    except KeyError:
        print('smth wrong')
    except pymysql.Error:
        print('smth wrong w/ bd')
    return {
        "status": "OK"
    }

# ----------------------creategame-----------------------------------------


def check_pw(pw: str) -> object:
    regex = re.compile('[^a-zA-Z0-9]')
    return regex.search(pw)


def get_hash():
    date = datetime.datetime.now()
    hasher = hashlib.md5(str(date).encode('utf-8'))
    h = str(base64.urlsafe_b64encode(hasher.digest()))
    an_filt = filter(str.isalnum, h)
    an_str = "".join(an_filt)[:3]
    return an_str


def create_game(event):
    h = get_hash()
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.CREATE_GAME_1.format(
        game_id=h,
        host=event['object']['message']['from_id'],
        passwd=event['object']['message']['text'],
    ))
    cur.execute(queries.UPD_HOST_1.format(
        game_id=h,
        new_stage=2,
        user_id=event['object']['message']['from_id']
    ))
    conn.commit()
    conn.close()
    return h


def process_password_cg(event):
    pw = event['object']['message']['text']
    bad_pass = check_pw(pw)
    if not bad_pass:
        h = create_game(event)
        msg = messages.messages['success_gc'].format(
            id=h,
            passwd=pw
        )
        keyboard = keyboards.keyboards['game_host']
    else:
        msg = messages.messages['failpass_gc']
        keyboard = keyboards.keyboards['back_only']
    return msg, keyboard


def process_payload_first(payload, event):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.UPDATE_STAGE_0.format(
        new_stage=stagetab.payloads['first'][payload]['next_stage'],
        user_id=event['object']['message']['from_id']
    ))
    conn.commit()
    conn.close()
    msg = messages.messages[stagetab.payloads['first'][payload]['msg']]
    keyboard = keyboards.keyboards[stagetab.payloads['first'][payload]['keyboard']]
    return msg, keyboard


def spyBotprod_creategame(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg, keyboard = process_password_cg(event)
        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['first']:
                msg, keyboard = process_payload_first(payload, event)
            else:
                msg = messages.messages['payload_err']
                keyboard = keyboards.keyboards['back_only']
        print(child.send_message(str(event['object']['message']['from_id']),
                                 msg, keyboard))
    except KeyError:
        print('smth wrong')
    except pymysql.Error:
        print('smth wrong w/ bd')
    return {
        "status": "OK"
    }

# ------------------------------initial---------------------------------


def process_payload_zero(payload, event):
    conn = pymysql.connect("spydatabase.crqx5vnl70pi.eu-north-1.rds.amazonaws.com", "admin", "12345678",
                           "Spy", connect_timeout=5)
    cur = conn.cursor()
    cur.execute(queries.UPDATE_STAGE_0.format(
        new_stage=stagetab.payloads['zero'][payload]['next_stage'],
        user_id=event['object']['message']['from_id']
    ))
    conn.commit()
    conn.close()
    msg = messages.messages[stagetab.payloads['zero'][payload]['msg']]
    keyboard = keyboards.keyboards[stagetab.payloads['zero'][payload]['keyboard']]
    return msg, keyboard


def spyBotprod_initial(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg = messages.messages['zero_error']
            keyboard = keyboards.keyboards['initial']

        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['zero']:
                msg, keyboard = process_payload_zero(payload, event)
            else:
                msg = messages.messages['payload_err']
                keyboard = keyboards.keyboards['initial']
        print(child.send_message(str(event['object']['message']['from_id']),
                                 msg, keyboard))
    except KeyError:
        print('smth wrong')
    except pymysql.Error:
        print('smth wrong w/ bd')
    return {
        "status": "OK"
    }
# ---------------------------------------------------------------
