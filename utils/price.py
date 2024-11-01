def price_format(price):
    return f'R$ {price:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
    return sum([item['quantity'] for item in cart.values()])
