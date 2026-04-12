from decimal import Decimal

from django import template
from django.template import TemplateSyntaxError

from ..money import Money
from ..utils import MONEY_CLASSES


register = template.Library()


class MoneyLocalizeNode(template.Node):
    def __repr__(self):
        return "<MoneyLocalizeNode %d %s>" % (self.money.amount, self.money.currency)

    def __init__(self, money=None, amount=None, currency=None, use_l10n=None, var_name=None):
        if money and (amount or currency):
            raise Exception('You can define either "money" or the "amount" and "currency".')

        self.money = money
        self.amount = amount
        self.currency = currency
        self.use_l10n = use_l10n
        self.var_name = var_name

    @classmethod
    def handle_token(cls, parser, token):

        pass

    def render(self, context):

        pass


@register.tag
def money_localize(parser, token):
    """
    Usage::

        {% money_localize <money_object> [ on(default) | off ] [as var_name] %}
        {% money_localize <amount> <currency> [ on(default) | off ] [as var_name] %}

    Example:

        The same effect:
        {% money_localize money_object %}
        {% money_localize money_object on %}

        Assignment to a variable:
        {% money_localize money_object on as NEW_MONEY_OBJECT %}

        Formatting the number with currency:
        {% money_localize '4.5' 'USD' %}

    Return::

        Money object

    """
    pass
