# pylint: disable=all

from django.views import View
from django.views.generic import DetailView
from django.shortcuts import redirect, resolve_url, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from product.models import Variation
from utils import utils
from .models import Order, OrderedItem
import stripe


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        return super().dispatch(*args, **kwargs)


class Payment(DispatchLoginRequired, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


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
                variation_id=v.get('id_variation'),
                price=v['quantitative_price'],
                promotional_price=v['promotional_quantitative_price'],
                quantity=v['quantity'],
                image=v['image']
            ) for v in cart.values()
        ]
        )

        return redirect(resolve_url(
            'order:payment',
            order.pk
        ))


class CheckoutSessionView(DispatchLoginRequired, DetailView):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            payment_method = request.POST.get('payment_method', 'card')

            session = stripe.checkout.Session.create(
                payment_method_types=[payment_method],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Compra no E-commerce',
                        },
                        'unit_amount': int(order.total * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=(
                    f'http://127.0.0.1:8000/order/success/{
                        order.pk}?session_id={{CHECKOUT_SESSION_ID}}'
                ),

                cancel_url=(
                    f"http://127.0.0.1:8000/order/canceled/{
                        order.pk}"
                )
            )

            return redirect(session.url)

        except Exception as e:
            messages.error(request, f'Erro ao iniciar pagamento: {str(e)}')
            return redirect('product:cart')

    def get(self, request, order_id):

        return HttpResponse("Método inválido", status=400)


class SuccessView(DispatchLoginRequired, View):
    template_name = 'order/success.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('profile:create')

        order_id = kwargs.get('order_id')

        if not order_id:
            return HttpResponse("Order ID não fornecido", status=400)

        order = get_object_or_404(Order, pk=order_id, user=self.request.user)
        session_id = self.request.GET.get('session_id')

        if not session_id:
            messages.error(self.request, 'Session ID não fornecido.')
            return redirect('order:payment', order.pk)

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if session['payment_status'] == 'paid':
                order.status = 'A'
                order.save()

                context = {
                    'title': 'Pagamento Confirmado',
                    'order': order
                }

                return render(self.request, self.template_name, context)

            else:
                messages.error(
                    self.request,
                    'Pagamento não confirmado. Tente novamente ou entre em'
                    ' contato com o suporte.'
                )
                return redirect('order:payment', order.pk)

        except stripe.error.StripeError as e:  # type: ignore
            messages.error(
                self.request, f'Erro na comunicação com o Stripe: {str(e)}')
            return redirect('order:payment', order.pk)

        except Exception as e:
            messages.error(
                self.request, f'Ocorreu um erro inesperado: {str(e)}')
            return redirect('order:payment', order.pk)


class CanceledView(DispatchLoginRequired, DetailView):
    template_name = 'order/canceled.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

    def get(self, *args, **kwargs):
        context = {
            'title': 'Payment Canceled '
        }
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('profile:create')

        return render(self.request, self.template_name, context)
