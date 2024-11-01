# pylint: disable=all
from django.shortcuts import (
    redirect, resolve_url, get_object_or_404, render  # type: ignore
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        # TODO: REMOVE THE LINES ABOVE
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        referer = self.request.META.get(
            'HTTP_REFERER', resolve_url('product:list'))
        id_variation = self.request.GET.get('vid')

        if not id_variation:
            messages.error(self.request, 'Product does not exist')
            return redirect(referer)

        variation = get_object_or_404(models.Variation, id=id_variation)
        stock_variation = variation.stock

        product = variation.product
        product_id = product.pk
        product_name = product.name
        variation_name = variation.name or ''
        unitary_price = variation.marketing_price
        promotional_unitary_price = variation.promotional_marketing_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(self.request, 'Insufficient stock.')
            return redirect(referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        if id_variation in cart:
            cart_quantity = cart[id_variation]['quantity']
            cart_quantity += 1

            if stock_variation < cart_quantity:
                messages.warning(
                    self.request, f'Insufficient stock for {cart_quantity}x '
                    f'of product "{product_name}". We added {stock_variation}x'
                    f' to your cart.')
                cart_quantity = stock_variation

            cart[id_variation]['quantity'] = cart_quantity

            cart[id_variation]['quantitative_price'] = (
                unitary_price * cart_quantity
            )

            cart[id_variation]['promotional_quantitative_price'] = (
                promotional_unitary_price * cart_quantity)  # type: ignore

        else:
            cart[id_variation] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'id_variation': id_variation,
                'unitary_price': unitary_price,
                'promotional_unitary_price': promotional_unitary_price,
                'quantitative_price': unitary_price,
                'promotional_quantitative_price': promotional_unitary_price,
                'quantity': quantity,

                'slug': slug,
                'image': image,
            }

        self.request.session.save()
        messages.success(
            self.request,
            f'The product {product_name} {variation_name} has '
            f'been added to the cart {cart[id_variation]["quantity"]}x.')

        return redirect(referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')
