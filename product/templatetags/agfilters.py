from django.template import Library
from utils.price import price_format, cart_total_qtd
register = Library()


@register.filter()
def formated_price(price: float):
    return price_format(price)


@register.filter()
def calculate_total_items(cart):
    return cart_total_qtd(cart)
