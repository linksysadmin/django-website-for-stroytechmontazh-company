import logging

from service.converting import convert_string_to_dict
from service.file_handler import create_excel_file

logger = logging.getLogger()


def create_offer(message, bot):
    data_dict = convert_string_to_dict(message.text)
    if data_dict:
        file = create_excel_file(data_dict)
        if file:
            with open(file, 'rb') as file:
                try:
                    bot.send_document(chat_id=message.chat.id, document=file,
                                            # caption=f'{ADDRESS}',
                                            disable_content_type_detection=True,
                                            visible_file_name=f'{data_dict["address"]}.xlsx')
                    bot.delete_state(message.from_user.id, message.chat.id)
                    logger.info(f'Файл удачно отправлен пользователю: {message.from_user.id}')
                except Exception as e:
                    logger.error(f'Неудачная отправка файла пользователю: {message.from_user.id}. Ошибка: {e}')
                    bot.send_message(message.chat.id, 'Попробуйте еще раз\n'
                                                      f'Ошибка:\n {e}')

    else:
        logger.error('Неверно введены данные от пользователя')
        bot.send_message(message.chat.id, 'Неверно введены данные')
        return



