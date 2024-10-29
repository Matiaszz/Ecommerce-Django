from django.template import Library
from utils.price import price_format
register = Library()


@register.filter()
def formated_price(price: float):
    return price_format(price)
