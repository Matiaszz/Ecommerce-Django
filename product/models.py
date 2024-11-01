# pylint: disable=fixme

"""Models"""
import os
from PIL import Image
from utils.price import price_format
from django.conf import settings
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

    # TODO: Remove blank and null on finish of project
    image = models.ImageField(
        upload_to='media/product_images%Y/%m/',
        blank=True, null=True)
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

    @staticmethod
    def resize_image(img, new_width=800):
        """Resize images

        Args:
            img (models.ImageField): receive a ImageField from django to resize

            new_width (int, optional): new width for the image.
            Defaults to 800.
        """
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img.file)
        original_width, original_height = img_pil.size
        if original_width <= new_width:
            img_pil.close()

            return
        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        new_img.save(img_full_path, optimize=True, quality=70)

        img_pil.close()
        return new_img

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug
        if self.image:
            max_image_size = 800
            self.resize_image(self.image, max_image_size)
        return super().save(*args, **kwargs)

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
