# Generated by Django 4.2.6 on 2023-10-18 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_cartitems_price_cartitems_cart_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='cart_price',
        ),
    ]
