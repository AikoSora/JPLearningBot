from aiogram.types import InlineKeyboardButton as IKB
from aiogram.types import InlineKeyboardMarkup as IKM
from aiogram.types.callback_query import CallbackQuery

from app.bot import handler
from app.models import Account

profile_inline_keyboard = IKM(inline_keyboard=[
    [IKB("Магазин", callback_data="shop")]
])


async def profile(event_object, path_args, bot, user):
    text = f"{user.first_name}さん, Ваш профиль:\n\n"
    text += f"Баланс: {user.balance}円\n"
    text += f"Рейтинг: {user.rating}\n"
    text += f"Кана: {user.kana_average_time}s. ({user.kana_rating_right}/10)\n"
    text += f"Числа: {user.numbers_average_time}s. ({user.numbers_rating_right}/10)\n"
    text += f'\nДата регистрации: {user.reg_date.strftime("%Y.%m.%d %H:%M")}'

    if type(event_object) == CallbackQuery:
        return await event_object.message.edit_text(text, reply_markup=profile_inline_keyboard)
    await user.reply(text, keyboard=profile_inline_keyboard)


@handler.message(names='профиль', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await profile(message, path_args, bot, user)


@handler.callback(name="profile")
async def _(callback, path_args, bot, user):
    await profile(callback, path_args, bot, user)
