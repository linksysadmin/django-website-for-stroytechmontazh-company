# -*- coding: utf-8 -*-
import logging

import colorlog
import flask
import telebot
from telebot import TeleBot
from telebot.storage import StateRedisStorage

from config import TELEGRAM_TOKEN, BASE_DIR
from handlers.register_functions import set_filters, set_commands, set_menu_commands

# LOGGING
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(name)s %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    })

file_handler = logging.FileHandler(f'{BASE_DIR}/logs/log.log')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logging.basicConfig(handlers=[file_handler], level=logging.INFO)
logger = logging.getLogger(__name__)
# END LOGGING


state_storage = StateRedisStorage()

bot = TeleBot(TELEGRAM_TOKEN, state_storage=state_storage, parse_mode='html')

set_menu_commands(bot)
set_filters(bot)
set_commands(bot)

# try:
#     bot.infinity_polling()
# except KeyboardInterrupt:
#     print('Выход из программы')

try:
    app = flask.Flask(__name__)

    @app.route('/', methods=['POST'])
    def webhook():
        """Обработка http-запросов, которые telegram пересылает на наш сервер"""
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            logger.error('abort(403)')
            flask.abort(403)
except Exception as e:
    logger.error(e)

