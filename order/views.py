# pylint: disable=all
from django.views import View
from django.http import HttpResponse


class Payment(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Payment')


class OrderDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Order Details')


class CloseOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Close Order')
