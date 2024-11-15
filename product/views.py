# pylint: disable=all

from django.shortcuts import (
    redirect, resolve_url, get_object_or_404, render  # type: ignore
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages
from django.db.models import Q
from . import models
from profiles.models import ProfileUser


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Início '
        return context


class Search(ListProduct):
    def get_queryset(self, *args, **kwargs):
        value = self.request.GET.get(
            'search') or self.request.session['search']
        qs = super().get_queryset(*args, **kwargs)

        if not value:
            return qs

        self.request.session['search'] = value

        qs = qs.filter(
            Q(name__icontains=value) |
            Q(short_description__icontains=value) |
            Q(long_description__icontains=value)
        )

        self.request.session.save()
        return qs


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Produto '
        return context


class AddToCart(View):
    def get(self, *args, **kwargs):

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
            f'O produto {product_name} {variation_name} foi '
            f'adicionado ao carrinho {cart[id_variation]["quantity"]}x.')

        return redirect(referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        referer = self.request.META.get(
            'HTTP_REFERER', resolve_url('product:list'))

        id_variation = self.request.GET.get('vid')

        if not self.request.session.get('cart'):
            return redirect(referer)

        if not id_variation:
            return redirect(referer)

        if id_variation not in self.request.session['cart']:
            return redirect(referer)

        cart = self.request.session['cart'][id_variation]

        messages.success(self.request,
                         f'O produto "{cart["product_name"]}"'
                         'foi removido.'
                         )

        del self.request.session['cart'][id_variation]

        self.request.session.save()
        return redirect(referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {}),
            'title': 'Carrinho ',
        }
        return render(self.request, 'product/cart.html', context)


class PurchaseSummary(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        profile = ProfileUser.objects.filter(user=self.request.user).exists()
        if not profile:
            messages.error(self.request, 'Usuário sem perfil')
            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.info(self.request, 'Carrinho vazio')
            return redirect('product:list')

        context = {
            'title': 'Resumo ',
            'user': self.request.user,
            'cart': self.request.session['cart']

        }
        return render(self.request, 'product/purchaseSummary.html', context)
