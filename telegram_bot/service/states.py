from telebot.handler_backends import StatesGroup, State


class MyStates(StatesGroup):
    create_offer = State()
