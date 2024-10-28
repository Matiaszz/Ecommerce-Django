# pylint: disable=all
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Payment.as_view(), name='payment'),

    path('closeorder/', views.CloseOrder.as_view(), name='closeorder'),

    path('details/', views.OrderDetails.as_view(),
         name='order_details'),

]
