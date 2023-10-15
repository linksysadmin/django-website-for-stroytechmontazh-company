from handlers.commands import *
from handlers.callback import *
import telebot


def set_filters(bot):
    """   Добавление фильтров сообщений   """
    from telebot.custom_filters import TextMatchFilter, IsDigitFilter, StateFilter
    from service.filters import CheckStringForOffer
    FILTERS = (StateFilter(bot),
               IsDigitFilter(),
               TextMatchFilter(),
               CheckStringForOffer(),)
    for filter_ in FILTERS:
        bot.add_custom_filter(filter_)


def set_menu_commands(bot):
    bot.delete_my_commands(scope=None, language_code=None)

    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "Начать"),
            telebot.types.BotCommand("offer", "Сформировать отчет"),
            telebot.types.BotCommand("clients", "Клиенты"),
            telebot.types.BotCommand("services", "Услуги"),
            telebot.types.BotCommand("cancel", "Отменить создание отчета"),
            telebot.types.BotCommand("log", "Файл логирования"),
        ], )


def set_commands(bot):
    bot.register_message_handler(commands=['start'], callback=start, pass_bot=True)
    bot.register_message_handler(commands=['clients'], callback=clients, pass_bot=True)
    bot.register_message_handler(commands=['services'], callback=services, pass_bot=True)
    bot.register_message_handler(commands=['offer'], callback=offer, pass_bot=True)
    bot.register_message_handler(commands=['cancel'], callback=cancel, pass_bot=True)
    bot.register_message_handler(commands=['log'], callback=log, pass_bot=True)
    bot.register_message_handler(state=MyStates.create_offer, callback=create_offer, pass_bot=True, string_for_offer=True)
    bot.register_message_handler(state=MyStates.create_offer, callback=incorrect_string_for_offer, pass_bot=True, string_for_offer=False)
