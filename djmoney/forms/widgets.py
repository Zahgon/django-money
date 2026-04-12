from django.forms import HiddenInput, MultiWidget, Select, TextInput

from ..settings import CURRENCY_CHOICES


__all__ = (
    "HiddenMoneyWidget",
    "MoneyWidget",
)


class HiddenMoneyWidget(HiddenInput):

    def format_value(self, value):
        pass


class MoneyWidget(MultiWidget):
    def __init__(
        self,
        choices=CURRENCY_CHOICES,
        amount_widget=TextInput,
        currency_widget=None,
        default_currency=None,
        *args,
        **kwargs,
    ):
        self.default_currency = default_currency
        if not currency_widget:
            currency_widget = Select(choices=choices)
        widgets = (amount_widget, currency_widget)
        super().__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        pass
