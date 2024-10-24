# pylint: disable=fixme

"""Models"""
from django.conf import settings
from django.db import models
from PIL import Image
import os


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

        Variation:
            name - char
            product - FK Product
            price - Float
            promotional_price - Float
            estoque - Int
    """

    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=70)
    long_description = models.TextField(max_length=255)

    # TODO: Remove blank and null on finish of project
    image = models.ImageField(
        upload_to='media/product_images%Y/%m/',
        blank=True, null=True)
    slug = models.SlugField(unique=True)
    marketing_price = models.FloatField()
    promotional_marketing_price = models.FloatField(
        default=0, blank=True, null=True)
    types = models.CharField(
        default='V', max_length=1,
        choices=(
            ('V', 'Variation'),
            ('S', 'Simple')
        )
    )

    @staticmethod
    def resize_image(img, new_width=800):
        """_summary_

        Args:
            img (models.ImageField): _description_
            new_width (int, optional): _description_. Defaults to 800.
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

        if self.image:
            max_image_size = 800
            self.resize_image(self.image, max_image_size)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Variation(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    marketing_price = models.FloatField()
    promotional_marketing_price = models.FloatField(
        default=0, blank=True, null=True)
    stock = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name
