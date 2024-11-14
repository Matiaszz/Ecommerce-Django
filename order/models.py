"""Models"""

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Order
        user - FK User
        total - Float
        status - Choices
            ('A', 'Aproved'),
            ('C', 'Created'),
            ('R', 'Reproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(default='c', max_length=1, choices=(
        ('A', 'Aproved'),
        ('C', 'Created'),
        ('R', 'Reproved'),
        ('P', 'Pending'),
        ('S', 'Sent'),
        ('F', 'Finished'),
    )
    )

    def __str__(self) -> str:
        return f'Order N° {self.pk}'


class OrderedItem(models.Model):
    """
        order - FK order
        product - Char
        product_id - Int
        variation - Char
        variation_id - Int
        price - Float
        promotional_price - Float
        quantity - Int
        image - Char (adress of image)
    """
    class Meta:
        """Meta
        Defines the plural name
        """
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveBigIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'Item do pedido N° {self.order}'
