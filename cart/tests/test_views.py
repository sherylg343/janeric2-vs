from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse

from django_libs.tests.mixins import ViewTestMixin

from .factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)
from products.models import Category, Product_Family, Product
from django.contrib.auth.models import User

from django.contrib.messages import get_messages


client = Client()


class CartViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'view_cart'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'cart/cart.html')

    def test_view_cart(self):
        category = CategoryFactory()
        product_family = Product_FamilyFactory()
        self.product1 = ProductFactory(
            category=category, product_family=product_family)
        self.product2 = ProductFactory(
            category=category, product_family=product_family)

        # NEED TO ADD PRODUCTS TO CART FIRST
        response = self.client.get(self.get_url())
        self.assertTrue(response.context['on_cart_page'], True)

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.product_family)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product2.product_family)


class AddToCartViewTestCase(ViewTestMixin, TestCase):
    """ Test for Add to Cart View """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(AddToCartViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'add_to_cart'

    def test_add_cart_view(self):
        pk = 2
        self.is_callable(kwargs={'product_id': pk})
