from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator
from django.db import models
from django.db.models import NOT_PROVIDED, F, Field, Func, Value
from django.db.models.expressions import BaseExpression
from django.db.models.signals import class_prepared
from django.utils.encoding import smart_str
from django.utils.functional import cached_property

from djmoney import forms
from djmoney.money import Currency, Money
from moneyed import Money as OldMoney

from .._compat import setup_managers
from ..settings import CURRENCY_CHOICES, CURRENCY_CODE_MAX_LENGTH, DECIMAL_PLACES, DEFAULT_CURRENCY
from ..utils import MONEY_CLASSES, get_currency_field_name, prepare_expression


__all__ = ("MoneyField",)


class MoneyValidator(DecimalValidator):
    def __call__(self, value):
        return super().__call__(value.amount)


def get_value(obj, expr):
    """
    Extracts value from object or expression.
    """
    pass


def validate_money_expression(obj, expr):
    """
    Money supports different types of expressions, but you can't do following:
      - Add or subtract money with not-money
      - Any exponentiation
      - Any operations with money in different currencies
      - Multiplication, division, modulo with money instances on both sides of expression
    """
    pass


def validate_money_value(value):
    """
    Valid value for money are:
      - Single numeric value
      - Money instances
      - Pairs of numeric value and currency. Currency can't be None.
    """
    pass


def get_currency(value):
    """
    Extracts currency from value.
    """
    pass


class MoneyFieldProxy:
    def __init__(self, field):
        self.field = field
        self.currency_field_name = get_currency_field_name(self.field.name, self.field)

    def _money_from_obj(self, obj):
        pass

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        data = obj.__dict__
        if isinstance(data[self.field.name], BaseExpression):
            return data[self.field.name]
        if not isinstance(data[self.field.name], Money):
            data[self.field.name] = self._money_from_obj(obj)
        return data[self.field.name]

    def __set__(self, obj, value):  # noqa
        if (
            value is not None
            and self.field._currency_field.null
            and not isinstance(value, MONEY_CLASSES)
            and not obj.__dict__[self.currency_field_name]
        ):
            # For nullable fields we need either both NULL amount and currency or both NOT NULL
            raise ValueError("Missing currency value")
        if isinstance(value, BaseExpression):
            if isinstance(value, Value):
                value = self.prepare_value(obj, value.value)
            elif not isinstance(value, Func):
                validate_money_expression(obj, value)
                prepare_expression(value)
        else:
            value = self.prepare_value(obj, value)
        obj.__dict__[self.field.name] = value

    def prepare_value(self, obj, value):
        pass

    def set_currency(self, obj, value):
        # we have to determine whether to replace the currency.
        # i.e. if we do the following:
        # .objects.get_or_create(money_currency='EUR')
        # then the currency is already set up, before this code hits
        # __set__ of MoneyField. This is because the currency field
        # has less creation counter than money field.
        #
        # Gotcha:
        # But we should also allow setting a field back to its original default
        # value!
        # https://github.com/django-money/django-money/issues/221
        pass


class CurrencyField(models.CharField):
    description = "A field which stores currency."

    def __init__(self, price_field=None, default=DEFAULT_CURRENCY, **kwargs):
        if isinstance(default, Currency):
            default = default.code
        kwargs.setdefault("max_length", CURRENCY_CODE_MAX_LENGTH)
        self.price_field = price_field
        super().__init__(default=default, **kwargs)

    def contribute_to_class(self, cls, name):
        pass


class MoneyField(models.DecimalField):
    description = "A field which stores both the currency and amount of money."

    @property
    def non_db_attrs(self):
        pass

    def __init__(
        self,
        verbose_name=None,
        name=None,
        max_digits=None,
        decimal_places=DECIMAL_PLACES,
        default=NOT_PROVIDED,
        default_currency=DEFAULT_CURRENCY,
        currency_choices=CURRENCY_CHOICES,
        currency_max_length=CURRENCY_CODE_MAX_LENGTH,
        currency_field_name=None,
        money_descriptor_class=MoneyFieldProxy,
        **kwargs,
    ):
        nullable = kwargs.get("null", False)
        default = self.setup_default(default, default_currency, nullable)

        # Provide the default currency from the default Money instance provided
        if not default_currency and isinstance(default, Money):
            default_currency = default.currency

        self.currency_max_length = currency_max_length
        self.default_currency = default_currency
        self.currency_choices = currency_choices
        self.currency_field_name = currency_field_name
        self.money_descriptor_class = money_descriptor_class

        super().__init__(verbose_name, name, max_digits, decimal_places, default=default, **kwargs)
        self.creation_counter += 1
        Field.creation_counter += 1

    def setup_default(self, default, default_currency, nullable):
        # None and NOT_PROVIDED are returned as-is
        pass

    def to_python(self, value):
        pass

    def clean(self, value, model_instance):
        """
        We need to run validation against ``Money`` instance.
        """
        pass

    @cached_property
    def validators(self):
        """
        Default ``DecimalValidator`` doesn't work with ``Money`` instances.
        """
        pass

    def contribute_to_class(self, cls, name):
        pass

    def add_currency_field(self, cls, name):
        """
        Adds CurrencyField instance to a model class.
        """
        pass

    def get_db_prep_save(self, value, connection):
        pass

    def get_default(self):
        pass

    @property
    def _has_default(self):
        # Whether the field has an explicitly provided non-empty default.
        # `None` was used by django-money before, and we need to check it because it can come from historical migrations
        pass

    def formfield(self, **kwargs):
        pass

    def value_to_string(self, obj):
        pass

    def deconstruct(self):
        pass


def patch_managers(sender, **kwargs):
    """
    Patches models managers.
    """
    pass


class_prepared.connect(patch_managers)
