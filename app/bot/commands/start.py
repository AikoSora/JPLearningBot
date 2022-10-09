from app.bot import handler
from app.models import Account


@handler.message(names='/start', dialog=Account.Dialog.START)
async def _(message, path_args, bot, user):
    user.dialog = Account.Dialog.DEFAULT
    user.save()
    await user.return_menu(f"{user.first_name}さん, Привет!")
