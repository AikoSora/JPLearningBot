from decimal import Decimal
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot import handler
from app.models import Account


shop_inline_keyboard = IKM(inline_keyboard=[
    [IKB("Рейтинг", callback_data="shop_rating")],
    [IKB("Назад", callback_data="profile")]
])
rating_cost = 100


def create_quantity_keyboard(command_name: str, cost: int, user: Account) -> IKM:
    max_rating = user.balance // cost
    max_buttons = max_rating if max_rating < 6 else 6
    button_text = 1
    ikm_array = []

    for x in range(2):
        ikb = []
        for x in range(3):
            if not max_buttons or button_text > max_rating:
                break

            ikb.append(IKB(f"{button_text}", callback_data=f"{command_name} {button_text}"))

            button_text += button_text
            max_buttons -= 1

        ikm_array.append(ikb)

    if max_rating:
        ikm_array.append([IKB(f"MAX {max_rating}", callback_data=f"{command_name} {max_rating}")])
    ikm_array.append([IKB("Назад", callback_data="shop")])

    return IKM(inline_keyboard=ikm_array)


@handler.callback(name="shop")
async def _(callback, path_args, bot, user):
    await callback.message.edit_text(f"{user.first_name}さん, Что вы хотите приобрести?", reply_markup=shop_inline_keyboard)


@handler.callback(name="shop_rating")
async def _(callback, path_args, bot, user):
    text = f"{user.first_name}さん "
    if user.balance > 99:
        text += "Выберите количество:"
    else:
        text += "Похоже у вас не достаточно денег m(._.)m"

    await callback.message.edit_text(text, reply_markup=create_quantity_keyboard("rating", rating_cost, user))


@handler.callback(name="rating")
async def _(callback, path_args, bot, user):
    if len(path_args) < 2 or not path_args[1].isdigit():
        return

    rating = int(path_args[1])
    money = rating * rating_cost
    extra_text = ""

    if user.balance - money < 0:
        return

    elif user.balance - money > 99:
        extra_text = "\nХотите приобрести еще?"

    user.balance -= Decimal(money)
    user.rating += rating
    user.save()

    await callback.message.edit_text(f"{user.first_name}さん, Вы приобрели {rating}ед. рейтинга за {money}円 (￣∀￣){extra_text}", reply_markup=create_quantity_keyboard("rating", rating_cost, user))
