from django.utils.module_loading import import_string

from djmoney.contrib.exchange.models import Rate

from ..base import BaseExchangeCommand


class Command(BaseExchangeCommand):
    help = "Clears exchange rates."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
