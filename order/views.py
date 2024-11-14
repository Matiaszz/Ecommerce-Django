# pylint: disable=all
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from product.models import Variation
from utils import utils
from .models import Order, OrderedItem


class Payment(View):
    def get(self, *args, **kwargs):
        return HttpResponse('pagarararara')


class OrderList(View):
    def get(self, *args, **kwargs):
        # context = {
        #     'title': 'Pagamento',
        #     'qtd_total_cart': qtd_cart,
        #     'total_value': cart_value_total
        # }
        return HttpResponse('Order list')


class OrderDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Order Details')


class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('profile:create')

        cart = self.request.session.get('cart')

        if not cart:
            messages.error(self.request, 'Não há produtos no carrinho.')
            return redirect('product:list')

        cart_items_variatons_ids = [v for v in cart]
        variations = list(
            Variation.objects.select_related('product').filter(
                id__in=cart_items_variatons_ids)
        )
        for variation in variations:
            vid = str(variation.pk)
            stock = variation.stock
            qtd_cart = cart[vid]['quantity']
            unit_price = cart[vid]['unitary_price']
            promotional_unit_price = cart[vid]['promotional_unitary_price']

            error_stock = ''

            if stock < qtd_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unit_price
                cart[vid]['promotional_quantitative_price'] = stock * \
                    promotional_unit_price

                error_stock = (
                    'Estoque insuficiente para alguns produtos do seu carrinho'
                    '. Reduzimos a quantidade desses produtos, por favor, '
                    'verifique quais produtos foram afetados.'
                )
            if error_stock:

                messages.error(
                    self.request, error_stock
                )
                self.request.session.save()
                return redirect('product:cart')

        cart_qtd_total = utils.cart_total_qtd(cart)
        cart_value_total = utils.cart_total_price(cart)

        order = Order(
            user=self.request.user,
            total=cart_value_total,
            qtd_total=cart_qtd_total,
            status='C'
        )
        order.save()

        OrderedItem.objects.bulk_create([
            OrderedItem(
                order=order,
                product=v['product_name'],
                product_id=v['product_id'],
                variation=v['variation_name'],
                variation_id=v.get('id_variation'),  # erro nessa linha
                price=v['quantitative_price'],
                promotional_price=v['promotional_quantitative_price'],
                quantity=v['quantity'],
                image=v['image']
            ) for v in cart.values()
        ]
        )

        del self.request.session['cart']
        # return render(self.request, self.template_name, context)
        return redirect('order:list')
