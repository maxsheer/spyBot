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

# ----------------------findgame-----------------------------------------

def process_id(event):


def spyBotprod_findgame(event, context):
    vk_api_key = os.environ['VK_API_KEY']
    vk_api_ver = os.environ['VK_API_VER']
    try:
        child = vkbot.VkBot(vk_api_key, vk_api_ver)
        if 'payload' not in event['object']['message']:
            msg, keyboard = process_id(event)
        else:
            payload = json.loads(event['object']['message']['payload'])['info']
            if payload in stagetab.payloads['fourth']:
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

# ----------------------hostgame-----------------------------------------


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
