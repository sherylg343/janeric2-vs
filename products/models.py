from django.db import models
from django.db.models.fields import IntegerField


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    division = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_division(self):
        return self.division

    def get_name(self):
        return self.name


class Product_Family(models.Model):
    class Meta:
        verbose_name_plural = 'Product_Families'

    name = models.CharField(max_length=254)
    brand_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_brand_name(self):
        return self.brand_name

    def get_name(self):
        return self.name


class Product(models.Model):
    SIZES = (
        ('8oz.', "8 oz."),
        ('16oz', "16 oz."),
        ('18oz', "18 oz."),
        ('32oz', "32 oz."),
        ('Gallon', "Gallon"),
        ('.9diameter', '.9 in. diameter'),
        ('2.6x12', '2.6 in. x 12 in.'),
        ('3.375x3.375', '3.375 in. x 3.375 in.'),
        ('3x4', '3 in. x 4 in.'),
        ('4inLength-custom avail', '4 in. length - custom available'),
        ('4x3.625', '4 in. x 3.625 in.'),
        ('4x6', '4 in. x 6 in.'),
        ('4x9', '4 in. x 9 in.'),
        ('4x18', "4 in. x 18 in."),
        ('6x9', '6 in. x 9 in.'),
        ('7x10', '7 in. x 10 in.'),
        ('7x17', '7 in. x 17 in.'),
        ('9x12', '9 in. x 12 in.'),
        ('9.125x2.1875x4.875', '9.125 in. x 2.1875 in. x 4.875 in.'),
        ('11x17', "11 in. x 17 in."),
        ('12x18', '12 in. x 18 in.'),
        ('12.125x16.875', '12.125 in. x 16.875 in.'),
        ('12x18', '12 in. x 18 in.'),
    )

    category = models.ForeignKey(
        'Category', null=True, on_delete=models.SET_NULL)
    product_family = models.ForeignKey(
        "Product_Family", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    SKU = models.CharField(
        max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    size = models.CharField(
        max_length=254, null=True, blank=True, choices=SIZES)
    pack = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True)

    def __str__(self):
        return self.name

