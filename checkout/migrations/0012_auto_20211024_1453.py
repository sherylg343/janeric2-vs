# Generated by Django 3.1.5 on 2021-10-24 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210911_1840'),
        ('checkout', '0011_shipping'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Shipping',
            new_name='ProductShippingData',
        ),
    ]
