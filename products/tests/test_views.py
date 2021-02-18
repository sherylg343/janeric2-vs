from django.test import TestCase, Client
from django.urls import reverse

from django_libs.tests.mixins import ViewTestMixin

from products.views import all_products
from .factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)


class AllProductsViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def setUp(self):
        self.category = CategoryFactory()
        self.product_family = Product_FamilyFactory()
        self.response = self.client.get(self.get_url())

    def get_view_name(self):
        return 'products'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_view_products(self):
        product1 = ProductFactory(
            category=self.category, product_family=self.product_family)
        product2 = ProductFactory(
            category=self.category, product_family=self.product_family)

        response = self.client.get(self.get_url())

        self.assertContains(response, product1.name)
        self.assertContains(response, product1.product_family)
        self.assertContains(response, product2.name)
        self.assertContains(response, product2.product_family)
