# pylint: disable=all
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pay/<int:pk>', views.Payment.as_view(), name='payment'),
    path('saveorder/', views.SaveOrder.as_view(), name='saveorder'),
    path('details/<int:order_id>',
         views.OrderDetails.as_view(), name='order_details'),
    path('list/', views.OrderList.as_view(), name='list'),
    path('checkout-session/<int:order_id>/',
         views.CheckoutSessionView.as_view(), name='checkout_session'),
    path(
        'success/<int:order_id>/', views.SuccessView.as_view(), name='sucess'),
]
