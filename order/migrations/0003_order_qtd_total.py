# Generated by Django 5.1.2 on 2024-11-14 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_ordeditem_ordereditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qtd_total',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
