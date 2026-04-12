from django.core.management.base import BaseCommand

from djmoney import settings


class BaseExchangeCommand(BaseCommand):
    """
    Basic command for exchange rates manipulation.
    Provides ``backend`` argument.
    """

    def add_arguments(self, parser):
        pass

    def success(self, message):
        pass
