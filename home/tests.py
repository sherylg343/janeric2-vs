from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse

from django_libs.tests.mixins import ViewTestMixin


client = Client()


class HomesViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'home'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'home/index.html')
