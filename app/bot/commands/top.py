from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot import handler
from app.models import Account
from django.db.models import Q

emoji_top = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

inline_keyboard_kana = IKM(inline_keyboard=[
    [IKB("Рейтинг", callback_data="rating_top"), IKB("Числа", callback_data="numbers_top")]
])

inline_keyboard_numbers = IKM(inline_keyboard=[
    [IKB("Кана", callback_data="kana_top"), IKB("Рейтинг", callback_data="rating_top")]
])

inline_keyboard_rating = IKM(inline_keyboard=[
    [IKB("Кана", callback_data="kana_top"), IKB("Числа", callback_data="numbers_top")]
])


async def top_function(user: Account, field: str, keyboard: IKM, callback=None) -> None:
    top_type = ("Кана" if field == "kana_average_time" else "Числа") if field != "rating" else "Рейтинг"
    text = f"{user.first_name}さん, Топ ({top_type}):\n\n"
    text_length = len(text)

    order_by_right = "numbers_rating_right" if field == "numbers_average_time" else "kana_rating_right"

    if field == "rating":
        query = Account.objects.filter(~Q(rating=0)).order_by("-rating")[:10]
    else:
        query = Account.objects.filter(~Q(**{order_by_right: 0, field: 0})).order_by(f"-{order_by_right}", field)[:10]

    for i, users in enumerate(query):
        if field == "rating":
            text += f"{emoji_top[i]} {users.first_name} - {users.rating}\n"

        elif field == "numbers_average_time":
            text += f"{emoji_top[i]} {users.first_name} - {int(users.numbers_average_time)}s. ({users.numbers_rating_right}/10)\n"

        elif field == "kana_average_time":
            text += f"{emoji_top[i]} {users.first_name} - {int(users.kana_average_time)}s. ({users.kana_rating_right}/10)\n"

    if len(text) == text_length:
        text += "Топ пустует m(._.)m"

    if callback:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await user.reply(text, keyboard=keyboard)


@handler.message(names='топ', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await top_function(user, "rating", inline_keyboard_rating)


@handler.callback(name='numbers_top')
async def _(callback, path_args, bot, user):
    await top_function(user, "numbers_average_time", inline_keyboard_numbers, callback)


@handler.callback(name='rating_top')
async def _(callback, path_args, bot, user):
    await top_function(user, "rating", inline_keyboard_rating, callback)


@handler.callback(name='kana_top')
async def _(callback, path_args, bot, user):
    await top_function(user, "kana_average_time", inline_keyboard_kana, callback)
