import datetime
import time
from decimal import Decimal
from json import dumps, loads
from random import choice, randint

from aiogram.types import InlineKeyboardButton as IKB
from aiogram.types import InlineKeyboardMarkup as IKM
from aiogram.types import KeyboardButton as KB
from aiogram.types import ReplyKeyboardMarkup as RKM

from app.bot import handler
from app.models import Account

inline_keyboard = IKM(inline_keyboard=[
    [IKB("Хирагана", callback_data="hiragana_test"), IKB("Катакана", callback_data="katakana_test")]
])

HIRAGANA = "hiragana"
KATAKANA = "katakana"

hiragana = [
    [("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o")],
    [("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko")],
    [("が", "ga"), ("ぎ", "gi"), ("ぐ", "gu"), ("げ", "ge"), ("ご", "go")],
    [("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so")],
    [("ざ", "za"), ("じ", "zi"), ("ず", "zu"), ("ぜ", "ze"), ("ぞ", "zo")],
    [("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to")],
    [("だ", "da"), ("ぢ", "di"), ("づ", "du"), ("で", "de"), ("ど", "do")],
    [("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no")],
    [("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho")],
    [("ば", "ba"), ("び", "bi"), ("ぶ", "bu"), ("べ", "be"), ("ぼ", "bo")],
    [("ぱ", "pa"), ("ぴ", "pi"), ("ぷ", "pu"), ("ぺ", "pe"), ("ぽ", "po")],
    [("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo")],
    [("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro")],
    [("や", "ya"), ("ゆ", "yu"), ("よ", "yo")],
    [("わ", "wa"), ("を", "wo"), ("ん", "n")]
]

katakana = [
    [("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")],
    [("カ", "ka"), ("キ", "ki"), ("ク", "ku"), ("ケ", "ke"), ("コ", "ko")],
    [("ガ", "ga"), ("ギ", "gi"), ("グ", "gu"), ("ゲ", "ge"), ("ゴ", "go")],
    [("サ", "sa"), ("シ", "shi"), ("ス", "su"), ("セ", "se"), ("ソ", "so")],
    [("ザ", "za"), ("ジ", "zi"), ("ズ", "zu"), ("ゼ", "ze"), ("ゾ", "zo")],
    [("タ", "ta"), ("チ", "chi"), ("ツ", "tsu"), ("テ", "te"), ("ト", "to")],
    [("ダ", "da"), ("ヂ", "di"), ("ヅ", "du"), ("デ", "de"), ("ド", "do")],
    [("ナ", "na"), ("ニ", "ni"), ("ヌ", "nu"), ("ネ", "ne"), ("ノ", "no")],
    [("ハ", "ha"), ("ヒ", "hi"), ("フ", "fu"), ("ヘ", "he"), ("ホ", "ho")],
    [("バ", "ba"), ("ビ", "bi"), ("ブ", "bu"), ("べ", "be"), ("ボ", "bo")],
    [("パ", "pa"), ("ピ", "pi"), ("プ", "pu"), ("ぺ", "pe"), ("ポ", "po")],
    [("マ", "ma"), ("ミ", "mi"), ("ム", "mu"), ("メ", "me"), ("モ", "mo")],
    [("ラ", "ra"), ("リ", "ri"), ("ル", "ru"), ("レ", "re"), ("ロ", "ro")],
    [("ヤ", "ya"), ("ユ", "yu"), ("ヨ", "yo")],
    [("ワ", "wa"), ("ヲ", "wo"), ("ン", "n")]
]


def get_symbol_from_kana(kana=None) -> tuple[str, str]:
    if kana is not None:
        kana = globals()[kana]
    else:
        kana = hiragana if randint(0, 1) else katakana

    column = choice(kana)
    row = choice(column)
    return row


def get_choice_keyboard(symbol: tuple):
    keyboard = []
    column, row = randint(0, 2), randint(0, 2)

    for i in range(3):
        kb = []
        for x in range(3):
            if column == i and row == x:
                kb.append(KB(f"{symbol}"))
            else:
                kb.append(KB(f"{get_symbol_from_kana()[1]}"))
        keyboard.append(kb)
    keyboard.append([KB("Назад")])

    return RKM(keyboard, resize_keyboard=True)


def add_time_in_database_array(user_object: Account, start: bool = False, right: bool = False):
    time_array = loads(user_object.kana_average_json_array)['data']
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

    user_object.kana_average_json_array = dumps({'data': time_array})


def get_user_average_time(user_object):
    data = loads(user_object.kana_average_json_array)['data']
    times = []

    for time_data in data:
        if time_data['time'][1][1]:
            times.append(time_data['time'][1][0] - time_data['time'][0][0])

    return sum(times) // len(times) if len(times) > 0 else 0


async def kana_test(message, path_args, bot, user):
    user.kana_test_count += 1

    if message.text.lower() == "назад":
        return await user.return_menu()

    data = get_symbol_from_kana(user.dialog)
    text = f"{user.first_name}さん, "

    keyboard = get_choice_keyboard(data[1])

    if message.text.lower() == user.kana_test_temp:
        add_time_in_database_array(user, right=True)
        user.balance += Decimal(10)
        user.kana_test_right += 1
        text += "Ответ правильный! Вот ваши 10円 ^ - ^!\n"

    else:
        add_time_in_database_array(user)
        text += f"Не правильно!, но не стоит расстраиваться! (^_^)\nОтвет был - <b>{user.kana_test_temp}</b>"

    if user.kana_test_count == 10:
        average_time = get_user_average_time(user)

        if (not user.kana_average_time or user.kana_average_time > average_time) and \
                (user.kana_rating_right < user.kana_test_right):

            user.kana_average_time = average_time
            user.kana_rating_right = user.kana_test_right

        user.kana_average_json_array = '{"data": []}'
        user.kana_test_count = 0
        user.kana_test_right = 0
        user.kana_test_time = time.time() + 3600
        user.save()
        return await user.return_menu(f"{text}\nТеперь отдохните, черезмерное увлечение тестами вредит вашему рвению что-либо выучить! ^ - ^")

    add_time_in_database_array(user, start=True)
    user.kana_test_temp = data[1]
    user.save()
    await user.reply(text + f"\nСледующий символ - <b>{data[0]}</b>", keyboard=keyboard)


@handler.message(names='/kana_data', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    await user.reply(user.kana_average_time)


@handler.message(names='кана', dialog=Account.Dialog.DEFAULT)
async def _(message, path_args, bot, user):
    if user.kana_test_time < time.time():
        await user.reply(f"{user.first_name}さん, Я буду вам писать символ каны, а вы должны будете выбрать правильный вариант в кнопках, за каждый правильный ответ буду начислять 10円!", keyboard=inline_keyboard)
    else:
        await user.reply(f"{user.first_name}さん, Подождите еще {datetime.timedelta(seconds = int(user.kana_test_time - time.time()))}")


@handler.callback(name='hiragana_test')
async def _(callback, path_args, bot, user):
    data = get_symbol_from_kana(HIRAGANA)

    user.dialog = Account.Dialog.HIRAGANA

    if user.kana_test_count == 0:
        add_time_in_database_array(user, start=True)

    user.kana_test_temp = data[1]
    user.save()

    await callback.message.delete()
    await user.reply(f"{user.first_name}さん Хорошо! Тогда твой первый символ - <b>{data[0]}</b>", keyboard=get_choice_keyboard(data[1]))


@handler.callback(name='katakana_test')
async def _(callback, path_args, bot, user):
    data = get_symbol_from_kana(KATAKANA)

    user.dialog = Account.Dialog.KATAKANA

    if user.kana_test_count == 0:
        add_time_in_database_array(user, start=True)

    user.kana_test_temp = data[1]
    user.save()

    await callback.message.delete()
    await user.reply(f"{user.first_name}さん Хорошо! Тогда твой первый символ - <b>{data[0]}</b>", keyboard=get_choice_keyboard(data[1]))


@handler.message(names='', dialog=Account.Dialog.HIRAGANA)
async def _(message, path_args, bot, user):
    await kana_test(message, path_args, bot, user)


@handler.message(names='', dialog=Account.Dialog.KATAKANA)
async def _(message, path_args, bot, user):
    await kana_test(message, path_args, bot, user)
