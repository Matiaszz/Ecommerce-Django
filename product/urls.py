# pylint: disable=all
from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('', views.ListProduct.as_view(), name='list'),

    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),

    path('search/', views.Search.as_view(), name='search'),

    path('addtocart/', views.AddToCart.as_view(), name='addtocart'),

    path('removefromcart/', views.RemoveFromCart.as_view(),
         name='removefromcart'),

    path('cart/', views.Cart.as_view(), name='cart'),

    path('purchasesummary/', views.PurchaseSummary.as_view(),
         name='purchasesummary'),
]
