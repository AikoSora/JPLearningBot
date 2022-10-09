from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB
from django.db import models


keyboard = RKM([
    [KB('Кана'), KB('Числа')],
    [KB('Профиль'), KB("Топ")]
], resize_keyboard=True)


class Account(models.Model):
    class TempData:
        bot = None

    class Dialog:
        START = 'start'
        DEFAULT = 'default'
        NUMBERS = "numbers"
        HIRAGANA = "hiragana"
        KATAKANA = "katakana"

    # Base variables
    user_id = models.BigIntegerField(null=False)
    first_name = models.TextField()
    last_name = models.TextField(default='', null=True, blank=True)
    username = models.TextField(default=None, null=True, blank=True)
    reg_date = models.DateTimeField(default=datetime.now())
    dialog = models.TextField(default=Dialog.START)
    temp = models.TextField(default='', blank=True)
    # extra variables
    balance = models.DecimalField(default=0, max_digits=32, decimal_places=0)
    rating = models.IntegerField(default=0)

    #Numbers
    numbers_test_count = models.IntegerField(default=0)
    numbers_test_right = models.IntegerField(default=0)
    numbers_test_time = models.IntegerField(default=0)
    numbers_test_temp = models.TextField(default="")
    numbers_average_json_array = models.TextField(default='{"data": []}')
    numbers_average_time = models.IntegerField(default=0)
    numbers_rating_right = models.IntegerField(default=0)

    #Kana
    kana_test_count = models.IntegerField(default=0)
    kana_test_right = models.IntegerField(default=0)
    kana_test_time = models.IntegerField(default=0)
    kana_test_temp = models.TextField(default='')
    kana_average_json_array = models.TextField(default='{"data": []}')
    kana_average_time = models.IntegerField(default=0)
    kana_rating_right = models.IntegerField(default=0)

    async def reply(self, text, **kwargs):
        processed_text = '\n'.join(text) if isinstance(text, list) else text
        return await self.TempData.bot.send_message(self.user_id, processed_text % kwargs['concate'] if 'concate' in kwargs else processed_text, parse_mode='HTML', reply_markup=(kwargs['keyboard'] if 'keyboard' in kwargs else None))

    async def return_menu(self, text='🚀 Вы зашли в <b>главное меню</b> бота', **kwargs):
        self.dialog = self.Dialog.DEFAULT
        self.save()
        return await self.reply(text, keyboard=keyboard, **kwargs)
