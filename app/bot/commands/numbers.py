import time
import datetime

from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot import handler
from app.models import Account
from random import randint
from decimal import Decimal
from json import dumps, loads


numbers = ["ぜろ", "いち", "に", "さん", "よん", "ご", "ろく", "なな", "はち", "きゅう"]
all = {10: "じゅう", 100: "ひゃく", 1000: "せん", 10000: "まん"}
exceptions = {300: "さんびゃく", 600: "ろっぴゃく", 800: "はっぴゃく", 3000: "さんぜん", 8000: "はっせん"}

keyboard = RKM([
    [KB('Назад')]
], resize_keyboard=True)

inline_keyboard = IKM(inline_keyboard=[
    [IKB("Начать", callback_data="start_numbers")]
])


def get_jp_text_from_number(number: int) -> str:
    if len(str(number)) == 1:
        return numbers[number]

    if number in exceptions:
        return exceptions[number]

    if number in all:
        return all[number]

    return None


def get_jp_number_text(number: int) -> str:
    """Function for translate numbers (max before 99999)"""
    if get_jp_text_from_number(number) is not None:
        return get_jp_text_from_number(number)

    lenght = len(str(number))
    text = ""

    for i, txt in enumerate(str(number)):
        if txt == "0":
            continue

        end_iteration = lenght - (i + 1)
        number_txt = ""
        if not get_jp_text_from_number(int(txt + ("0" * end_iteration))):
            number_txt = get_jp_text_from_number(int(txt))
            if end_iteration != 0:
                number_txt += get_jp_text_from_number(int("1" + ("0" * end_iteration)))
        else:
            number_txt += get_jp_text_from_number(int(txt + ("0" * end_iteration)))
        text += number_txt if number_txt != "まん" else "いちまん"

    return text


def get_random_number_and_text() -> tuple[int, str]:
    number = randint(0, 99999)
    return (number, get_jp_number_text(number))


def add_time_in_database_array(user_object: Account, start: bool = False, right: bool = False):
    time_array = loads(user_object.numbers_average_json_array)['data']
    time_object = {"time": []}
    length_array = len(time_array)
    time_object_array = [time.time()]

    if length_array > 0 and not start:
        time_object = time_array[length_array - 1]
        if len(time_object) > 1:
            time_object = {"time": []}

    if not start:
        time_object_array.append(right)

    time_object['time'].append(time_object_array)

    if start:
        time_array.append(time_object)

    user_object.numbers_average_json_array = dumps({'data': time_array})


def get_user_average_time(user_object):
    data = loads(user_object.numbers_average_json_array)['data']
    times = []

    for time_data in data:
        if time_data['time'][1][1]:
            times.append(time_data['time'][1][0] - time_data['time'][0][0])

    return sum(times) // len(times) if len(times) > 0 else 0


@handler.message(names='/user_array', dialog=Account.Dialog.DEFAULT, with_args=True)
async def _(message, path_args, bot, user):
    if len(path_args) > 1:
        if path_args[1] == "reset":
            user.numbers_average_json_array = '{"data": []}'

        if path_args[1] == "add":
            if len(path_args) > 2:
                kwargs = {}
                for args in path_args[2:]:
                    kwargs.update({f'{args}': True})
                add_time_in_database_array(user, **kwargs)

            else:
                add_time_in_database_array(user)

        user.save()

        if path_args[1] == "show":
            if len(path_args) > 2:
                if path_args[2] == "average":
                    await user.reply(user.numbers_average_time)
            else:
                await user.reply(user.numbers_average_json_array)


@handler.message(names='числа', dialog=Account.Dialog.DEFAULT, with_args=True)
async def _(message, path_args, bot, user):
    if user.numbers_test_time < time.time():
        await user.reply(f"{user.first_name}さん, Я буду говорить тебе числа, а ты должен будешь написать их хираганой, за правильный ответ буду начислять 50円! Если ты готов, нажми кнопку - <i>Начать</i>", keyboard=inline_keyboard)
    else:
        await user.reply(f"{user.first_name}さん, Подождите еще {datetime.timedelta(seconds = int(user.numbers_test_time - time.time()))}")


@handler.callback(name='start_numbers')
async def _(callback, path_args, bot, user):
    data = get_random_number_and_text()
    user.dialog = Account.Dialog.NUMBERS
    user.numbers_test_temp = data[1]
    add_time_in_database_array(user, True)
    user.save()

    await callback.message.delete()
    await user.reply(f"{user.first_name}さん Хорошо! Тогда твое первое число - <b>{data[0]}</b>", keyboard=keyboard)


@handler.message(names='', dialog=Account.Dialog.NUMBERS)
async def _(message, path_args, bot, user):
    user.numbers_test_count += 1

    if message.text.lower() == "назад":
        return await user.return_menu()

    data = get_random_number_and_text()
    text = f"{user.first_name}さん, "

    if user.numbers_test_temp == message.text:
        text += "Ответ правильный! Вот ваши 50円 (*´꒳`*)"
        add_time_in_database_array(user, right=True)
        user.numbers_test_right += 1
        user.balance += Decimal(50)
    else:
        add_time_in_database_array(user)
        text += f"Не правильно!, но не стоит расстраиваться! (^_^)\nОтвет был - <b>{user.numbers_test_temp}</b>"

    if user.numbers_test_count == 10:
        average_time = get_user_average_time(user)

        if not user.numbers_average_time or user.numbers_average_time > average_time:
            user.numbers_average_time = average_time

        if user.numbers_rating_right < user.numbers_test_right:
            user.numbers_rating_right = user.numbers_test_right

        user.numbers_average_json_array = '{"data": []}'
        user.numbers_test_count = 0
        user.numbers_test_right = 0
        user.numbers_test_time = time.time() + 3600
        user.save()
        return await user.return_menu(f"{text}\nТеперь отдохните, черезмерное увлечение тестами вредит вашему рвению что-либо выучить! ^ - ^")

    add_time_in_database_array(user, start=True)
    user.numbers_test_temp = data[1]
    user.save()
    await user.reply(text + f"\n<b>Следующее число</b> - {data[0]}")
