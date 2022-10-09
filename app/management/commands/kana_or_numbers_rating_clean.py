from django.core.management.base import BaseCommand
from app.models import Account
from django.db.models import Q


class Command(BaseCommand):
    help = 'Clean rating (kana/numbers)'

    def handle(self, *args, **options):
        for user in Account.objects.filter(~Q(kana_average_time=0) | ~Q(numbers_average_time=0)):
            user.kana_average_time = 0
            user.numbers_average_time = 0
            user.kana_rating_right = 0
            user.numbers_rating_right = 0
            user.save()
