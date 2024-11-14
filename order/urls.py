# pylint: disable=all
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Payment.as_view(), name='payment'),

    path('saveorder/', views.SaveOrder.as_view(), name='saveorder'),

    path('details/', views.OrderDetails.as_view(),
         name='order_details'),

    path('list/', views.OrderList.as_view(),
         name='list'),

]
