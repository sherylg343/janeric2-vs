from django.test import TestCase, Client

from django_libs.tests.mixins import ViewTestMixin


client = Client()


class ShippingViewTestCase(ViewTestMixin, TestCase):
    """ Tests for shipping view """
    def get_view_name(self):
        return 'shipping'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'shipping/shipping.html')
