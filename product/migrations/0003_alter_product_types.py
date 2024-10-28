# Generated by Django 5.1.2 on 2024-10-28 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_promotional_marketing_price_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='types',
            field=models.CharField(choices=[('V', 'Variable'), ('S', 'Simple')], default='V', max_length=1),
        ),
    ]