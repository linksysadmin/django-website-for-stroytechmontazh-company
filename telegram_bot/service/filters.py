import telebot


class CheckStringForOffer(telebot.custom_filters.SimpleCustomFilter):
    key = 'string_for_offer'

    def check(self, message):
        string_message = message.text

        if '|' not in string_message:
            return False
        else:
            return True
