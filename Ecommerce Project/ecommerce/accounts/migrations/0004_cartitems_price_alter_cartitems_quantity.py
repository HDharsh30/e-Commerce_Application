# Generated by Django 4.2.5 on 2023-10-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_cartitems_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
