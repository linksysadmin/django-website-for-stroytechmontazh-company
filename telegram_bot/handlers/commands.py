import logging

from config import BASE_DIR
from service.render import render
from service.models import session, Service, Feedback
from service.states import MyStates

logger = logging.getLogger()


def start(message, bot):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logger.info(f"ID: {user_id} | Имя: {user_name}")
    bot.send_message(user_id, render('start.html', {'name': user_name}))


def clients(message, bot):
    user_id = message.from_user.id
    feedbacks = session.query(Feedback).all()
    context = {
        'feedbacks': feedbacks,
    }
    bot.send_message(user_id, render('feedbacks.html', context=context))


def services(message, bot):
    user_id = message.from_user.id
    services_ = session.query(Service).all()
    context = {
        'services': services_,
    }
    bot.send_message(user_id, render('services.html', context))


def offer(message, bot):
    user_id = message.from_user.id
    services_ = session.query(Service).all()
    context = {
        'services': services_,
    }
    bot.set_state(message.from_user.id, MyStates.create_offer, message.chat.id)
    bot.send_message(user_id, render('services.html', context))
    bot.send_message(user_id, 'Для того, чтобы сформировать документ вам нужно ввести данные: (Адрес, услуги)\n'
                              'Если есть дополнительные услуги - введите "+ название услуги:стоимость за ед.:количество\n'
                              'Вот пример:\n')
    bot.send_message(user_id, 'Адрес | 1:5 2:6 3:7 + промывка бочка:5000:2 + промывка трубы:7000:2')
    logger.info(f'Состояние пользователя - {bot.get_state(message.from_user.id, message.chat.id)}')


def cancel(message, bot):
    bot.send_message(message.from_user.id, 'Создание отчета отменено')
    bot.delete_state(message.from_user.id, message.chat.id)
    logger.info(f'Создание отчета отменено')


def log(message, bot):
    logger.info(f'Получение log-файла')
    with open(f'{BASE_DIR}/logs/log.log', 'rb') as file:
        bot.send_document(chat_id=message.chat.id, document=file,
                          # caption=f'{ADDRESS}',
                          disable_content_type_detection=True,
                          visible_file_name=f'log.log')
    bot.delete_state(message.from_user.id, message.chat.id)


def incorrect_string_for_offer(message, bot):
    bot.send_message(message.from_user.id, 'Неверный ввод')
    logger.warning(f'Некорректный ввод данных для отчета')
