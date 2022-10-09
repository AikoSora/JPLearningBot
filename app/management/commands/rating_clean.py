from django.core.management.base import BaseCommand
from app.models import Account
from django.db.models import Q


class Command(BaseCommand):
    help = 'Clean rating'

    def handle(self, *args, **options):
        for user in Account.objects.filter(~Q(rating=0)):
            user.rating = 0
            user.save()
