from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.module_loading import import_string

from djmoney.settings import CURRENCY_CODE_MAX_LENGTH, EXCHANGE_BACKEND, RATES_CACHE_TIMEOUT

from .exceptions import MissingRate


class ExchangeBackend(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    last_update = models.DateTimeField(auto_now=True)
    base_currency = models.CharField(max_length=CURRENCY_CODE_MAX_LENGTH)

    def __str__(self):
        return self.name

    def clear_rates(self):
        pass


class Rate(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    currency = models.CharField(max_length=CURRENCY_CODE_MAX_LENGTH)
    value = models.DecimalField(max_digits=20, decimal_places=6)
    backend = models.ForeignKey(ExchangeBackend, on_delete=models.CASCADE, related_name="rates")

    class Meta:
        unique_together = (("currency", "backend"),)


def get_default_backend_name():
    pass


def get_rate(source, target, backend=None):
    """
    Returns an exchange rate between source and target currencies.
    Converts exchange rate on the DB side if there is no backends with given base currency.
    Uses data from the default backend if the backend is not specified.
    """
    pass


def _get_rate(source, target, backend):
    pass


def _try_to_get_rate_directly(source, target, rate):
    """
    Either target or source equals to base currency of existing rate.
    """
    pass


def _get_rate_via_base(rates, target):
    """
    :param: rates: A set/tuple of two base Rate instances
    :param: target: A string instance of the currency to convert to

    Both target and source are not a base currency - actual rate could be calculated via their rates to base currency.
    For example:

    7.84 NOK = 1 USD = 8.37 SEK

    7.84 NOK = 8.37 SEK

    1 NOK = 8.37 / 7.84 SEK
    """
    pass


def convert_money(value, currency, backend=None):
    pass
