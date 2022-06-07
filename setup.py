from os import system, name
from time import sleep


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

setup_import = input(f"{cy}install library {gr}yes{cy} / {re}no{cy}\n Enter the: ")


def banner():

    system("cls")
    print(
          f"       {re}─╔═╗{cy}─────────────────{re}╔╗{cy}\n"
          f"       {re}─║╔╝{cy}─────────────────{re}║║{cy}\n"
          f"       {re}╔╝╚╗{cy}╔══╗{re}╔═╗{cy}╔╗╔╗╔══╗{re}╔═╝║{cy}\n"
          f"       {re}╚╗╔╝{cy}║╔╗║{re}║╔╝{cy}║╚╝║║╔╗║{re}║╔╗║{cy}\n"
          f"       {re}─║║─{cy}║╚╝║{re}║║─{cy}╚╗╔╝║╔╗║{re}║╚╝║{cy}\n"
          f"       {re}─╚╝─{cy}╚══╝{re}╚╝──{cy}╚╝─╚╝╚╝{re}╚══╝{cy}\n"
          f"        by https://github.com/Forvad"
    )


def setup():
    print(
        f"{cy}╔═══╗╔═══╗╔════╗╔╗─╔╗╔═══╗\n"
        f"{cy}║╔═╗║║╔══╝║╔╗╔╗║║║─║║║╔═╗║\n"
        f"{cy}║╚══╗║╚══╗╚╝║║╚╝║║─║║║╚═╝║\n"
        f"{cy}╚══╗║║╔══╝──║║──║║─║║║╔══╝\n"
        f"{cy}║╚═╝║║╚══╗──║║──║╚═╝║║║───\n"
        f"{cy}╚═══╝╚═══╝──╚╝──╚═══╝╚╝───\n"
    )
    print(gr+"  [+] Installing  ...\n\n")
    sleep(3)
    if 'posix' in name:
        system("pip3 install requests==2.25.1 loguru==0.5.3 urllib3==1.26.8 "
               "TgCrypto==1.2.3 gunicorn==20.1.0 PySocks==1.7.1 pyTelegramBotAPI==4.3.1 configparser msvcrt")
    else:
        system("pip install requests==2.25.1 loguru==0.5.3 urllib3==1.26.8 "
               "TgCrypto==1.2.3 gunicorn==20.1.0 PySocks==1.7.1 pyTelegramBotAPI==4.3.1 configparser msvcrt")
    print('')
    print(gr+"[+]  Installed.\n")


def config_setup():
    import configparser
    data = configparser.RawConfigParser()
    data.add_section('data')
    auth = input(gr+"[+] enter authorization : "+re)
    data.set('data', 'auth', auth)
    server_chanel = input(gr+"[+] discord.com/.../... : "+re)
    data.set('data', 'server/chanel', server_chanel)
    use_telegram = (input(gr+'message TG (y/N): '+re))
    if use_telegram in ('y', 'Y'):
        bot_token = input(gr+'token bot Telegram: '+re)
        data.set('data', 'bot_token', bot_token)
        tg_user_id = input(gr+'UserID TG:  '+re)
        data.set('data', 'tg_user_id', tg_user_id)
    else:
        data.set('data', 'bot_token', 'no')
        data.set('data', 'tg_user_id', 'no')
    config = open('config.data', 'w')
    data.write(config)
    config.close()
    print(gr+"[+] setup complete !")


banner()
if setup_import in "yes":
    setup()
config_setup()
