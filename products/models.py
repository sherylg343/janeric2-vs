from django.db import models
from django.db.models.fields import IntegerField

from datetime import date


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
    class Meta:
        ordering = ['category__division', 'category__name', 'product_family__name', 'product_size']

    category = models.ForeignKey(
        'Category', null=True, on_delete=models.SET_NULL)
    product_family = models.ForeignKey(
        "Product_Family", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    SKU = models.CharField(
        max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    product_size = models.ForeignKey(
        "ProductSize", null=True, blank=True, on_delete=models.SET_NULL
    )
    pack = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    class Meta:
        ordering = ['name',]
        verbose_name_plural = 'Product Sizes'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

