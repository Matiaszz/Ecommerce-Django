# pylint: disable=fixme

"""Models"""
import io
from PIL import Image
from utils.utils import price_format
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    """Product Model

    Product:
            name - Char
            short_description - Text
            long_description - Text
            image - Image
            slug - Slug
            marketing_price - Float
            promotional_marketing_price - Float
            types - Choices
                ('V', 'Variable'),
                ('S', 'Simple'),
    """

    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=70)
    long_description = models.TextField(max_length=255)

    image = models.ImageField(
        upload_to='media/product_images%Y/%m/')
    slug = models.SlugField(unique=True, null=True, blank=True)
    marketing_price = models.FloatField()
    promotional_marketing_price = models.FloatField(
        default=0, blank=True, null=True)
    types = models.CharField(
        default='V', max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple')
        )
    )

    def get_price_formated(self):
        """
        Get the price of product and format them
        """

        return price_format(self.marketing_price) \
            if self.marketing_price is not None else 'N/A'

    get_price_formated.short_description = 'Price'

    def get_promotional_price_formated(self):
        """
        Get the promotional price of product and format them
        """

        return price_format(self.promotional_marketing_price)  \
            if self.promotional_marketing_price is not None else 'N/A'

    get_promotional_price_formated.short_description = 'Promotional Price'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.image:
            self.image.open()
            self.resize_image(self.image, 800)

        super().save(*args, **kwargs)

    def resize_image(self, image_field, max_size):
        img = Image.open(image_field)

        if img.height > max_size or img.width > max_size:
            output_size = (max_size, max_size)
            img.thumbnail(output_size)

            img_io = io.BytesIO()
            img.save(img_io, format=img.format)
            image_field.file = img_io
            image_field.file.seek(0)

    def __str__(self):
        return str(self.name)


class Variation(models.Model):
    """Variation
        name - char
        product - FK Product
        price - Float
        promotional_price - Float
        stock - Int
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    marketing_price = models.FloatField()
    promotional_marketing_price = models.FloatField(
        default=0, blank=True, null=True)
    stock = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name
