from django.test import TestCase, RequestFactory
from django.urls import reverse

from django_libs.tests.mixins import ViewTestMixin
from mixer.backend.django import mixer

from products.views import all_products
from products.models import Product


class AllProductsViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """

    def get_data_payload(self):
        if hasattr(self, 'data_payload'):
            return self.data_payload
        return {'foo': 'bar', }

    def test_get_name(self):
        resp = self.get_view_name()
        self.assertEqual(resp, 'all_products')

    def test_get(self):
        product = mixer.blend(Product, name='test gel')
        assert product.name == "test gel"

        self.data_payload = {"name": product.name}

        self.is_callable(message="Is callable with product name")
