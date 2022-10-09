import os
import importlib
import re
import uvloop

from aiogram import Bot, Dispatcher, executor, types
from app.models import Account
from app.bot import handler
from pathlib import Path


class TelegramBot:
    def __init__(self, **kwargs):
        if 'auth_token' not in kwargs:
            raise Exception('Not enough arguments to initialize the bot')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.__bot = Bot(token=kwargs['auth_token'])
        self.__dp = Dispatcher(self.__bot)
        Account.TempData.bot = self.__bot
        self.read_handlers()
        self.create_listeners()
        executor.start_polling(self.__dp, skip_updates=True)

    def load_or_create(self, user_obj):
        return Account.objects.get_or_create(user_id=user_obj.id, defaults={'first_name': user_obj.first_name, 'last_name': user_obj.last_name, 'username': user_obj.username})[0]

    def create_listeners(self):
        @self.__dp.message_handler()
        async def _(message: types.Message):
            processed_name = message.text.lower().strip()
            path_args = re.split(r'\s+', processed_name)
            user = self.load_or_create(message['from'])
            if 'меню' in processed_name:    # Check user wants return to menu
                await user.return_menu()
            else:
                for command in handler.commands:
                    if ((not command.with_args and command.name in ['', processed_name]) or (command.with_args and command.name in ['', path_args[0]])) and (command.dialog == user.dialog or command.dialog == "all"):
                        if not await command.handle(message, path_args, self.__bot, user):
                            await message.reply('❌ Произошла <b>системная</b> ошибка. Выйдите в меню и попробуйте <b>ещё раз</b>.', parse_mode='HTML')
                        break
                else:
                    await message.reply('⚠️ Неизвестная команда. Напишите мне <b>«Меню»</b> и воспользуйтесь кнопками', parse_mode='HTML')

        @self.__dp.callback_query_handler()
        async def _(call: types.CallbackQuery):
            path_args = re.split(r'\s+', call.data)
            user = self.load_or_create(call.from_user)
            for callback in handler.callbacks:
                if callback.name == path_args[0]:
                    if not await callback.handle(call, path_args, self.__bot, user):
                        await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Возникла ошибка при обработке события', show_alert=True)
                    break
            else:
                await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Неизвестный запрос', show_alert=True)

    def read_handlers(self):
        path = Path(__file__).resolve().parent.joinpath("commands/")

        for command in path.rglob('**/*.py'):

            spec = importlib.util.spec_from_file_location(
                command.name, command
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
