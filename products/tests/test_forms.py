from django.test import TestCase, RequestFactory
from django_libs.tests.mixins import ViewTestMixin

from products.forms import ProductForm, ProductFamilyForm

from products.models import Category, Product_Family, Product
from .factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)


class ProductFormTestCase(ViewTestMixin, TestCase):
    # Test if form is valid
    def test_form_valid(self):
        product = ProductFactory()
        data = {
            'name': product.name,
            'category': product.category,
            'product_family': product.product_family,
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_not__valid(self):
        product = ProductFactory()
        data = {
            'name': "",
            'category': product.category,
            'product_family': product.product_family,
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())


class ProductFamilyFormTestCase(ViewTestMixin, TestCase):
    # Test if form is valid
    def test_form_valid(self):
        product_family = Product_FamilyFactory()
        data = {
            'name': product_family.name,
            'brand_name': product_family.brand_name,
        }
        form = ProductFamilyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_not__valid(self):
        product_family = Product_FamilyFactory()
        data = {
            'name': "",
            'brand_name': product_family.brand_name,
        }
        form = ProductFamilyForm(data=data)
        self.assertFalse(form.is_valid())
