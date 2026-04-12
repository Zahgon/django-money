import json
import sys

import django
from django.core.serializers.base import DeserializationError
from django.core.serializers.json import Serializer as JSONSerializer

from djmoney.money import Money

from .models.fields import MoneyField
from .utils import get_currency_field_name


Serializer = JSONSerializer


def Deserializer(stream_or_string, **options):  # noqa
    """
    Deserialize a stream or string of JSON data.
    """
    pass
