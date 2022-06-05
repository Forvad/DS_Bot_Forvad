import threading
import requests
from time import sleep
from json import loads
from os import system
from ctypes import windll
from sys import stderr
from loguru import logger
from urllib3 import disable_warnings
from telebot import TeleBot
from telebot import apihelper




token_set: list = open('token.txt', 'r', encoding='utf-8').read().splitlines()
server_chat_id = input('discord.com/channels/.../...\nEnter the\n').split('/')
use_telegram = str(input('message TG (y/N): '))


def telegram_user():
    global tg_user_id
    global bot_token
    global tg_number_msg
    bot_token = str(input('token bot Telegram:\nEnter the\n '))
    tg_user_id = int(input('UserID TG:\nEnter the\n '))
    tg_number_msg = [25, 50, 75, 100, 200, 300, 400, 500]


def telegram_message(number):
    bot = TeleBot(bot_token)
    bot_msg_resp = str(bot.send_message(int(tg_user_id), f'написано {number} сообщений'))
    if 'from_user' in bot_msg_resp:
        logger.success(f'Сообщение в Telegram успешно отправлено')
    else:
        logger.error(f'Ошибка при отправке сообщения в Telegram: {bot_msg_resp}')


if use_telegram in ('y', 'Y'):
    telegram_user()



def token_verification(auth):
    session = requests.Session()
    session.headers['authorization'] = auth
    r = session.get(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=50')
    if r.status_code == 200 and len(loads(r.text)) > 0:
        return logger.success(f'Token Valid {auth}')
    else:
        return logger.error(f'Token False {auth} ')


disable_warnings()
logger.remove()
logger.add(stderr,
            format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> - <level>{message}</level>")
print('\nTelegram  - @Slava1133\n')
windll.kernel32.SetConsoleTitleW('Discord Bot | by Forvad')
for auth in token_set:
    token_verification(auth)


msg_set: list = open('msg.txt', 'r', encoding='latin-1').read().splitlines()
msg_sleep = int(input('message sleep\nEnter the\n'))
start_message = int(input(f'start messege 0...{(len(msg_set))}\nEnter the\n'))

def search(msg):
    session = requests.Session()
    session.headers['authorization'] = token_set[0]
    r = session.get(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=100')
    for text in loads(r.text):
        message = str(text['content']).replace('\n', '').replace('\r', '')
        id = str(text['id']).replace('\n', '').replace('\r', '')
        if message in msg:
            return id

def the_first_message(number):
    session = requests.Session()
    session.headers['authorization'] = token_set[0]
    r = session.post(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=50',
        json={'content': msg_set[number], 'tts': False})
    logger.success(f'сообщение отправлено пользователем R1 #{start_message}  -- {msg_set[number]}')

def messege():
    number_msg = start_message + 1
    the_first_message(start_message)
    sleep(msg_sleep)
    j = 1
    while True:
        if use_telegram in ('y', 'Y'):
            if number_msg in tg_number_msg:
                telegram_message(number_msg)
        msg = msg_set[number_msg]
        msg_search = msg_set[number_msg-1]
        session = requests.Session()
        session.headers['authorization'] = token_set[j]
        r = session.post(
            f'https://discord.com/api/v9/channels/{server_chat_id[1]}/messages?limit=50',
            json={'content': msg, 'tts': False,
                  'message_reference': {'channel_id': server_chat_id[1], 'guild_id': server_chat_id[0],
                                        "message_id": search(msg_search)
                                        }})
        if r.status_code == 200 and len(loads(r.text)) > 0:
            if j == 0:
                auth = 'R1'
            else:
                auth = 'R2'
            logger.success(f'сообщение отправлено пользователем {auth} #{number_msg}  -- {msg}')
            number_msg += 1
            if j == 1:
                j -= 1
            elif j == 0:
                j += 1
        else:
            logger.error('Произошла ошибка при отправке сообщения')
            if use_telegram in ('y', 'Y'):
                end_works = str(bot.send_message(int(tg_user_id), f'Произошла ошибка бот не отправил сообщение'))
        sleep(msg_sleep)
messege()
if use_telegram in ('y', 'Y'):
    end_works = str(bot.send_message(int(tg_user_id), f'end works'))

