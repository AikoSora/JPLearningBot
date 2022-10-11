from app.bot import handler
from app.models import Account, keyboard


@handler.message(names='/start', dialog=Account.Dialog.START)
async def _(message, path_args, bot, user):
    user.dialog = Account.Dialog.DEFAULT
    user.save()
    await user.reply(f"{user.first_name}さん, Привет!\nСоветую тебе прочитать сначала эту статью (//∇//)<a href='https://telegra.ph/JPLearning-Bot-10-09'>&#8203;</a>", keyboard=keyboard)
