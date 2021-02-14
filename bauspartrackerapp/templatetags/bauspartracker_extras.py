import logging

from django import template
from moneyed import Money


register = template.Library()


@register.filter
def percentage(value, arg):
    """
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    """
    try:
        percent_value = float( arg )
        if percent_value:
            return round(value / 100 * percent_value, 2)
    except Exception:
        pass
    return ''


@register.filter
def saldo(buchungen):
    """
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    """
    try:
        if buchungen:
            result = Money(0, 'EUR')
            for buchung in buchungen.all():
                result += buchung.betrag
            return result
    except Exception:
        pass
    return ''

