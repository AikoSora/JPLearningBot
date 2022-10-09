from django.core.management.base import BaseCommand
from django.conf import settings
from app.bot import TelegramBot


class Command(BaseCommand):
    help = 'Start Telegram bot'

    def handle(self, *args, **options):
        TelegramBot(auth_token=settings.BOT_TOKEN)
