from django.core.exceptions import ValidationError
from django.forms import ChoiceField, DecimalField, MultiValueField

from djmoney.money import Money
from djmoney.utils import MONEY_CLASSES

from ..settings import CURRENCY_CHOICES, DECIMAL_PLACES
from .widgets import HiddenMoneyWidget, MoneyWidget


__all__ = ("MoneyField",)


class MoneyField(MultiValueField):
    def __init__(
        self,
        currency_widget=None,
        currency_choices=CURRENCY_CHOICES,
        max_value=None,
        min_value=None,
        max_digits=None,
        decimal_places=DECIMAL_PLACES,
        default_amount=None,
        default_currency=None,
        *args,
        **kwargs,
    ):

        amount_field = DecimalField(
            *args,
            max_value=max_value,
            min_value=min_value,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs,
        )
        currency_field = ChoiceField(choices=currency_choices)

        self.widget = MoneyWidget(
            amount_widget=amount_field.widget,
            currency_widget=currency_widget or currency_field.widget,
            default_currency=default_currency,
        )
        # The two fields that this widget comprises
        fields = (amount_field, currency_field)

        super().__init__(fields, *args, **kwargs)

        # set the initial value to the default currency so that the
        # default currency appears as the selected menu item

        # Callables might be supplied in cases where the initial data is directly copied from the MoneyField db
        # object - this seems to happen internally when Django auto-generates certain hidden input fields to track
        # initial data in a formset.
        if callable(default_currency):
            default_currency = default_currency()

        # TODO: are we sure we do not have default_amount callables here?
        if isinstance(default_amount, Money):
            default_amount = default_amount.amount

        self.initial = [default_amount, default_currency]

    def hidden_widget(self):
        # TODO: This should inherit the constraints of the field
        #  Otherwise, we won't validate that min, max value and currency_choices are valid?
        # This is usually used to pre-fill the 'initial data' hidden input, so it's not very sensitive to tampering.
        pass

    def compress(self, data_list):
        pass

    def clean(self, value):
        pass

    def has_changed(self, initial, data):  # noqa
        pass
