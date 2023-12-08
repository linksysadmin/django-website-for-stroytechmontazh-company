import logging

import requests
import re

from django.conf import settings
from django.template.loader import get_template

logger = logging.getLogger(__name__)


def send_message_to_telegram(user_data):
    logger.info(f'Отправка данных клиента {user_data['name']} в телеграмм: ')
    phone = format_phone_number(user_data['phone'])
    context = {'name': user_data['name'], 'phone': phone}
    text = get_template('services/message.html')
    text_content = text.render(context)

    params = {
        'chat_id': settings.TELEGRAM_GROUP_CHAT_ID,
        'text': text_content
    }
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
    response = requests.post(url, params)
    response.raise_for_status()


def format_phone_number(string):
    cleaned_number = re.sub(r'\D', '', string)  # Оставляем только цифры
    if len(cleaned_number) == 11 and cleaned_number.startswith('8'):
        cleaned_number = '7' + cleaned_number[1:]  # Заменяем "8" на "7" в российских номерах
    return f"+{cleaned_number}"
