from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse
from django.conf import settings as django_settings

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
        response = self.client.get(self.get_url())
        self.assertTrue(response.context['on_cart_page'], True)


class AddToCartViewTestCase(ViewTestMixin, TestCase):
    """ Test for Add to Cart View """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        super(AddToCartViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'add_to_cart'

    def test_add_cart_view(self):
        cart_items = []
        total = 0
        quantity = 2
        product = self.product1
        product_id = self.product1.id
        product.price = 10.00
        product_count = quantity
        total = quantity * product.price
        print('--------qty:', quantity)
        print('---------price', product.price)
        shipping = total * .10
        grand_total = shipping + total

        cart_items = {
            'product_id': product_id,
            'quantity': quantity,
            'product_count': product_count,
        }
        session = self.client.session
        session['cart_items'] = cart_items
        session['total'] = total
        session['product_count'] = product_count
        session['shipping'] = shipping
        session['grand_total'] = grand_total
        session['quantity'] = quantity
        session.save()

        # Update session's cookie
        session_cookie_name = django_settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie_name] = session.session_key
        quantity1 = session['quantity']
        print("------session qty:", quantity1)

        response = self.client.get(
            self.get_url(view_kwargs={'product_id': product_id}))
        self.is_callable(kwargs={'product_id': product_id})
        self.assertTrue(response.context['quantity'], quantity)
        self.assertTrue(response.context['product'], product)
        self.assertTrue(response.context['product_count'], product_count)
        self.assertTrue(response.context['shipping'], shipping)
        self.assertTrue(response.context['grand_total'], grand_total)

# error: quantity = int(request.POST.get('quantity'))
# TypeError: int() argument must be a string, a bytes-like # object or a number, not 'NoneType'