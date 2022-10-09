#from app.models import Account
#from app.bot.assets import ToResponse
import traceback
import sys
#import re


# def send_report(user, message, traceback):
#     print(traceback)
#     for developer in Account.objects.filter(developer=True).all():
#         r = developer.reply(ToResponse.DEBUG_REPORT, concate=(user.full_name, user.username, user.dialog, message, traceback,))


class Command:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler', 'admin'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name'].lower()
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']
        self.admin = kwargs['admin']
        self.with_args = kwargs['with_args']

    async def handle(self, message, path_args, bot, user):
        try:
            await self.__handler(message, path_args, bot, user)
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            #send_report(user, message.text, '<b>%s</b>\n%s' % (ex, re.sub(r'/<>', '', str(traceback.format_tb(tb)))))
            return False


class Callback:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler', 'admin'}:
            raise Exception('Not enough arguments to create callback object')
        self.name = kwargs['name'].lower()
        self.__handler = kwargs['handler']
        self.admin = kwargs['admin']

    async def handle(self, callback, path_args, bot, user):
        try:
            await self.__handler(callback, path_args, bot, user)
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            #send_report(user, callback.data, '<b>%s</b>\n%s' % (ex, re.sub(r'/<>', '', str(traceback.format_tb(tb)))))
            return False
