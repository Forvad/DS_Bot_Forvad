from pyuseragents import random as random_useragent
from requests import Session, get, post
from setup import Update
from time import sleep
from json import loads
from os import system, name
from sys import stderr
from loguru import logger
from urllib3 import disable_warnings
from telebot import TeleBot
from telebot import apihelper
from configparser import RawConfigParser


class App:
    def __init__(self, auth, proxy, chat, server, token, user_id):
        self.chat_id = chat
        self.server_id = server
        self.authorization = auth
        self.proxy = proxy
        self.tg_user_id = user_id
        self.user_agent = [random_useragent(), random_useragent()]
        self.TG_bot = TeleBot(token)
        self.session = Session()
        self.session.headers.update({
            'sec-ch-ua-platform': 'Windows',
            'accept-language': 'ru-BY,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
            'accept-encoding': 'gzip, deflate, br',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'x-debug-options': 'bugReporterEnabled',
            'discord-locale': 'ru'})
        self.x_super_properties = ['eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lz'
                                  'dGVtX2xvY2FsZSI6InJ1LVJVIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbm'
                                  'Rvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSB'
                                  'HZWNrbykgQ2hyb21lLzk3LjAuNDY5Mi43MSBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9'
                                  'uIjoiOTcuMC40NjkyLjcxIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJp'
                                  'bmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3Vy'
                                  'cmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiO'
                                  'jEzMjEwOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=', 'eyJvcyI6IldpbmRvd3MiLCJicm9'
                                  '3c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1LVJVIiwiYnJvd3Nlcl'
                                  '91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGV'
                                  'XZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk3LjAuNDY5Mi43MSBTYWZhcmkvN'
                                  'ZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJkaXNjb3JkLmNvbSIs'
                                  'InJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2N'
                                  'oYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMzIzMjAsImNsaWVudF9ldmVudF9zb3V'
                                  'yY2UiOm51bGx9']

    def headers(self, number):
        if proxy_on:
            self.session.proxies.update({
                'http': f'http://{self.proxy[number]}',
                'https': f'http://{self.proxy[number]}'})
        self.session.headers['authorization'] = self.authorization[number]
        self.session.headers['user-agent'] = self.user_agent[number]
        self.session.headers['x-super-properties'] = self.x_super_properties[number]

    def end_of_work(self):
        bot_msg_resp = str(self.TG_bot.send_message(self.tg_user_id, f'''End of work\n 
        written messages: {len(msg_set)}'''))
        if 'from_user' in bot_msg_resp:
            logger.success('Telegram message has been sent successfully')
        else:
            logger.error(f'Error when sending a message to Telegram: {bot_msg_resp}')

    def telegram_message(self, number):
        bot_msg_resp = str(self.TG_bot.send_message(self.tg_user_id, f'written № {number} messages'))
        if 'from_user' in bot_msg_resp:
            logger.success('Telegram message has been sent successfully')
        else:
            logger.error(f'Error when sending a message to Telegram: {bot_msg_resp}')

    def token_verification(self, number):
        self.headers(number)
        r = self.session.get(
            f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=50')
        if r.status_code == 200 and len(loads(r.text)) > 0:
            return logger.success(f'Token Valid {self.authorization[number]}')
        else:
            return logger.error(f'Token False {self.authorization[number]} ')

    def search(self, msg):
        self.headers(number_auth)
        r = self.session.get(
            f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=100')
        for text in loads(r.text):
            message = str(text['content']).replace('\n', '').replace('\r', '')
            message_id = str(text['id']).replace('\n', '').replace('\r', '')
            if message in msg:
                return message_id

    def the_first_message(self):
        self.headers(0)
        self.session.post(
            f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=50',
            json={'content': msg_set[start_message], 'tts': False})
        logger.success(f'The message was sent by the user R1 #{int(start_message) + 1}  -- {msg_set[start_message]}')

    def message(self):
        global number_auth
        number_msg = int(start_message) + 1
        sleep(msg_sleep)
        number_auth = 1
        while number_msg < len(msg_set):
            if use_telegram in ('y', 'Y'):
                if number_msg + 1 in tg_number_msg:
                    self.telegram_message(number_msg + 1)
            msg = msg_set[number_msg]
            msg_search = msg_set[number_msg - 1]
            self.headers(number_auth)
            r = self.session.post(
                f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=50',
                json={'content': msg, 'tts': False,
                      'message_reference': {'channel_id': self.chat_id, 'guild_id': self.server_id,
                                            "message_id": self.search(msg_search)
                                            }})
            if r.status_code == 200 and len(loads(r.text)) > 0:
                if number_auth == 0:
                    user = 'R1'
                else:
                    user = 'R2'
                logger.success(f'The message was sent by the user {user} #{number_msg + 1}  -- {msg}')
                number_msg += 1
                if number_auth == 1:
                    number_auth -= 1
                elif number_auth == 0:
                    number_auth += 1
            else:
                logger.error('An error occurred while sending the message')
            sleep(msg_sleep)

Setup = Update()
if 'posix' in name:
    pass
else:
    Setup.banner()

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


config_data = input(f"{cy}do I need to change the config? {gr}yes{cy} / {re}no{cy}\n Enter the: ").lower()
if config_data in 'yes':
    Setup.config_setup()

msg_set: list = open('msg.txt', 'r', encoding='latin-1').read().splitlines()
# database of messages from the msg.text text file

data = RawConfigParser()
data.read('config.data')
token_set = data['data']['auth'].split(',')
server_chat_id = data['data']['server/chanel'].split('/')
bot_token = data['data']['bot_token']
tg_user_id = int(data['data']['tg_user_id'])
if len(data['data']['proxy']) > 1:
    proxy_on = True
    proxy = data['data']['proxy'].split(',')
else:
    proxy = data['data']['proxy']
    proxy_on = False
# loading from data with config.date

tg_number_msg = [25, 50, 75, 100, 200, 300, 400, 500]  # number of telegram notification messages
if bot_token in 'no':
    use_telegram = 'N'
else:
    use_telegram = 'Y'
disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> - <level>{message}</level>")
settings = App(auth=token_set, proxy=proxy, chat=server_chat_id[1], server=server_chat_id[0],
               token=bot_token, user_id=tg_user_id)
for i in range(2):
    settings.token_verification(i)

msg_sleep = int(input(gr+'message sleep:'+re))
start_message = int(input(gr+f'start message 1...{(len(msg_set)-1)}: '+re))

settings.the_first_message()
settings.message()
# the work of the bot
if use_telegram in 'Y':
    settings.end_of_work()
