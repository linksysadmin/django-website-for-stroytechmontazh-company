import requests

from django.conf import settings
from django.template.loader import get_template


def send_message(user_data):
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
    text = get_template('flushing/message.html')
    context = {'name': user_data['name'], 'phone': user_data['phone']}
    text_content = text.render(context)
    print(text_content)

    params = {
        'chat_id': settings.TELEGRAM_GROUP_CHAT_ID,
        'text': text_content
    }
    response = requests.post(url, params)
    response.raise_for_status()
