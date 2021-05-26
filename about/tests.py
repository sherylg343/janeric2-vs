from django.test import TestCase, Client

from django_libs.tests.mixins import ViewTestMixin


client = Client()


class AboutViewTestCase(ViewTestMixin, TestCase):
    """ Tests for home view """
    def get_view_name(self):
        return 'about'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'about/about.html')
