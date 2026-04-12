import json
import ssl
from decimal import Decimal
from typing import Optional
from urllib.parse import parse_qsl, urlparse, urlunparse
from urllib.request import Request, urlopen

from django.db.transaction import atomic
from django.utils.http import urlencode

from djmoney import settings

from ..models import ExchangeBackend, Rate


try:
    import certifi
except ImportError:
    raise ImportError("Please install dependency certifi - pip install certifi")


class BaseExchangeBackend:
    name: Optional[str] = None
    url: Optional[str] = None

    def get_rates(self, **kwargs):
        """
        Returns a mapping <currency>: <rate>.
        """
        raise NotImplementedError

    def get_url(self, **params):
        """
        Updates base url with provided GET parameters.
        """
        pass

    def get_params(self):
        """
        Default GET parameters for the request.
        """
        pass

    def get_response(self, **params):
        pass

    def parse_json(self, response):
        pass

    @atomic
    def update_rates(self, base_currency=settings.BASE_CURRENCY, **kwargs):
        """
        Updates rates for the given backend.
        """
        pass


class SimpleExchangeBackend(BaseExchangeBackend):
    """
    Simple backend implementation.
    Assumes JSON response with `rates` key inside.
    """

    def get_rates(self, **params):
        pass
