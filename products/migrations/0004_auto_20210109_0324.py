# Generated by Django 3.1.4 on 2021-01-09 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201210_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('8oz.', '8 oz.'), ('16oz', '16 oz.'), ('18oz', '18 oz.'), ('32oz', '32 oz.'), ('Gallon', 'Gallon')], max_length=254, null=True),
        ),
    ]
