from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings as django_settings
from django.contrib.sessions.middleware import SessionMiddleware

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

    def test_get(self):
        product1_id = self.product1.id
        product1 = self.product1
        product_name = product1.name
        product1.price = '10.00'
        product1.save()
        quantity1 = 5
        redirect_url = '/products/{product_id}/'.format(product_id=product1_id)
        quantity1 = 5
        quantity2 = 3
        product_count1 = quantity1
        product_count2 = quantity1 + quantity2
        session = self.client.session
        session['cart'] = {}
        session.save()

        data1 = {
            "id": product1_id,
            "name": product_name,
            'quantity': quantity1,
            'product': product1,
            'redirect_url': redirect_url,
        }

        # test content of first post
        add_url1 = reverse('add_to_cart', kwargs={'product_id': product1_id})
        response1_add = self.client.post(add_url1, data=data1, follow=True)
        self.assertEqual(response1_add.status_code, 200)
        self.assertContains(response1_add, product_count1)

        # Message appears adding new item to cart
        messages = list(get_messages(response1_add.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), f'Added {product_name} to your cart')

        # Test adding a quantity to an existing quantity
        data2 = {
            'product_id': product1_id,
            'name': product_name,
            'quantity': quantity2,
            'product': product1,
            'redirect_url': redirect_url,
        }

        # test post response status 200
        add_url2 = reverse('add_to_cart', kwargs={'product_id': product1_id})
        response2_add = self.client.post(add_url2, data=data2, follow=True)
        self.assertEqual(response2_add.status_code, 200)

        # test product data added to context and post
        self.assertContains(response2_add, product_count2)

        # test redirects to proper page
        self.assertRedirects(
            response2_add, '/products/1/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        # message that change quantity for product
        messages = list(get_messages(response2_add.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), f'Added {product_name} to your cart', 'Updated {product_name} quantity to {product_count2}')


class AdjustCartViewTestCase(ViewTestMixin, TestCase):
    """ Test for Add to Cart View """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()

        super(AdjustCartViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'adjust_cart'

    def test_get(self):
        product1_id = self.product1.id
        product1 = self.product1
        product_name = product1.name
        product1.price = '10.00'
        product1.save()
        quantity1 = 5
        redirect_url = '/products/{product_id}/'.format(product_id=product1_id)
        quantity3 = 1
        quantity4 = 0
        product_count3 = quantity3
        product_count4 = quantity4
        session = self.client.session
        session['cart'] = {}
        session.save()

        data3 = {
            'product_id': product1_id,
            'product': product1,
            'quantity': quantity3,
            'redirect_url': redirect_url,
        }

        # test content of first post
        adj_url1 = reverse('adjust_cart', kwargs={'product_id': product1_id})
        response1_adj = self.client.post(adj_url1, data=data3, follow=True)
        self.assertEqual(response1_adj.status_code, 200)
        self.assertContains(response1_adj, product_count3)

        # Message appears item quantity in cart
        messages = list(get_messages(response1_adj.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), f'Updated {product_name} quantity to {quantity3}')

        # Change product quantity to 0
        data4 = {
            'product_id': product1_id,
            'quantity': quantity4,
        }

        # test deletes quantity changed to zero
        adj_url4 = reverse('adjust_cart', kwargs={'product_id': product1_id})
        print("-------------adj_url4:", adj_url4)
        #response1_adj = self.client.post(adj_url4, data=data4, follow=True)
        #self.assertEqual(response1_adj.status_code, 200)

        # test redirects to proper page
        self.assertRedirects(
            response1_adj, '/cart/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        # Message appears item quantity in cart if item deleted
        #messages = list(get_messages(response1_adj.wsgi_request))
        #self.assertEqual(len(messages), 2)
        #for m in messages:
        #    self.assertEqual(
        #        str(m), f'Removed {product_name} from your bag', 'Updated {product_name} quantity to {quantity3}')
