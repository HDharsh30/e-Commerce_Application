# Generated by Django 4.2.6 on 2023-10-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_cartitems_price_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='price',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='cart_price',
            field=models.IntegerField(default=0),
        ),
    ]
