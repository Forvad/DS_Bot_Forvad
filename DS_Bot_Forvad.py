import requests
from time import sleep
from json import loads
from os import system
from sys import stderr
from loguru import logger
from urllib3 import disable_warnings
from telebot import TeleBot
from telebot import apihelper
from configparser import RawConfigParser
from msvcrt import getch


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def banner():
    print(
          f"       {re}─╔═╗{cy}─────────────────{re}╔╗{cy}\n"
          f"       {re}─║╔╝{cy}─────────────────{re}║║{cy}\n"
          f"       {re}╔╝╚╗{cy}╔══╗{re}╔═╗{cy}╔╗╔╗╔══╗{re}╔═╝║{cy}\n"
          f"       {re}╚╗╔╝{cy}║╔╗║{re}║╔╝{cy}║╚╝║║╔╗║{re}║╔╗║{cy}\n"
          f"       {re}─║║─{cy}║╚╝║{re}║║─{cy}╚╗╔╝║╔╗║{re}║╚╝║{cy}\n"
          f"       {re}─╚╝─{cy}╚══╝{re}╚╝──{cy}╚╝─╚╝╚╝{re}╚══╝{cy}\n"
          f"        by https://github.com/Forvad\n"
          f"         Telegram  - @Forvad1"
    )


msg_set: list = open('msg.txt', 'r', encoding='latin-1').read().splitlines()
data = RawConfigParser()
data.read('config.data')
token_set = data['data']['auth'].split(',')
server_chat_id = data['data']['server/chanel'].split('/')
bot_token = data['data']['bot_token']
tg_user_id = int(data['data']['tg_user_id'])
tg_number_msg = [25, 50, 75, 100, 200, 300, 400, 500]
if bot_token in 'no':
    use_telegram = 'N'
else:
    use_telegram = 'Y'
disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> - <level>{message}</level>")
banner()
msg_sleep = int(input(gr+'message sleep:'+re))
start_message = int(input(gr+f'start message 0...{(len(msg_set)-1)}: '+re))


def telegram_message(number):
    bot = TeleBot(bot_token)
    bot_msg_resp = str(bot.send_message(tg_user_id, f'written № {number} messages'))
    if 'from_user' in bot_msg_resp:
        logger.success('Telegram message has been sent successfully')
    else:
        logger.error(f'Error when sending a message to Telegram: {bot_msg_resp}')


def token_verification(author):
    session = requests.Session()
    session.headers['authorization'] = author
    r = session.get(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=50')
    if r.status_code == 200 and len(loads(r.text)) > 0:
        return logger.success(f'Token Valid {auth}')
    else:
        return logger.error(f'Token False {auth} ')


def search(msg):
    session = requests.Session()
    session.headers['authorization'] = token_set[0]
    r = session.get(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=100')
    for text in loads(r.text):
        message = str(text['content']).replace('\n', '').replace('\r', '')
        message_id = str(text['id']).replace('\n', '').replace('\r', '')
        if message in msg:
            return message_id


def the_first_message(number):
    session = requests.Session()
    session.headers['authorization'] = token_set[0]
    r = session.post(
        f'https://discord.com/api/v9/channels/{int(server_chat_id[1])}/messages?limit=50',
        json={'content': msg_set[number], 'tts': False})
    logger.success(f'The message was sent by the user R1 #{start_message+1}  -- {msg_set[number]}')


def messege():
    number_msg = start_message + 1
    the_first_message(start_message)
    sleep(msg_sleep)
    j = 1
    while number_msg < len(msg_set):
        if use_telegram in ('y', 'Y'):
            if number_msg + 1 in tg_number_msg:
                telegram_message(number_msg + 1)
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
                user = 'R1'
            else:
                user = 'R2'
            logger.success(f'The message was sent by the user {user} #{number_msg+1}  -- {msg}')
            number_msg += 1
            if j == 1:
                j -= 1
            elif j == 0:
                j += 1
        else:
            logger.error('An error occurred while sending the message')
        sleep(msg_sleep)


system("cls")
banner()
for auth in token_set:
    token_verification(auth)
sleep(2)
messege()
if use_telegram in ('y', 'Y'):
    bot = TeleBot(bot_token)
    end_works = str(bot.send_message(int(tg_user_id), f'end works'))
print('Press any key to exit...')
getch()
