# pylint: disable=all
from django.shortcuts import redirect, reverse, get_object_or_404  # type: ignore
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
        referer = self.request.META.get(
            'HTTP_REFERER', reverse('product:list'))
        id_variation = self.request.GET.get('vid')

        if not id_variation:
            messages.error(self.request, 'Produto não encontrado.')
            return redirect(referer)

        variation = get_object_or_404(models.Variation, id=id_variation)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        if id_variation in cart:
            # TODO: Exists variation in cart
            pass
        else:
            # TODO: Variation dont existis in cart

            pass
        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')
