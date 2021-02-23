from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django_libs.tests.mixins import ViewTestMixin

from products.views import all_products
from .factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)
from products.models import Category, Product_Family, Product
from django.contrib.auth.models import User


client = Client()


class AllProductsViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'products'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_view_products(self):
        category = CategoryFactory()
        product_family = Product_FamilyFactory()
        self.product1 = ProductFactory(
            category=category, product_family=product_family)
        self.product2 = ProductFactory(
            category=category, product_family=product_family)

        response = self.client.get(self.get_url())

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.product_family)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product2.product_family)


class AddProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(AddProductViewTestCase, cls).setUpClass()

    def test_database_size(self):
        self.assertEqual(len(Product.objects.all()), 4)

    def get_view_name(self):
        return 'add_product'

    def test_view_uses_correct_template(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.response = self.client.get(reverse(self.get_view_name()))
        self.assertTemplateUsed(self.response, 'products/add.html')

    def test_add_product_view(self):
        # case 1 - Anonymous User
        self.is_not_callable()
        # case 2 - superuser
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.is_callable()

    def test_database_add(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.product5 = ProductFactory()
        self.assertEqual(len(Product.objects.all()), 5)


class EditProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(EditProductViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'edit_product'

    def get_view_kwargs(self):
        return {'product_id': '2'}

    def test_view_uses_correct_template(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.response = self.client.get(
            reverse(self.get_view_name(), self.get_view_kwargs()))
        self.assertTemplateUsed(self.response, 'products/edit/2.html')

    def test_edit_product_view(self):
        # case 1 - Anonymous User
        self.is_not_callable()
        # case 2 - superuser
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.is_callable()

    def test_database_update(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.product4.name = 'Product Name Changed'
        self.product4.save()
        self.assertEqual(self.product4.name, 'Product Name Changed')


class DeleteProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(DeleteProductViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'delete_product'

    def get_view_kwargs(self):
        return {'pk': '2'}

    def test_view_uses_correct_template(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.response = self.client.get(
            reverse(self.get_view_name(), self.get_view_kwargs()))
        self.assertTemplateUsed(
            self.response, 'products/delete/2.html')

    def test_delete_product_view(self):
        # case 1 - Anonymous User
        self.is_not_callable()
        # case 2 - superuser
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.is_callable()

    def test_database_delete(self):
        self.user = User.objects.get_or_create(username="admin111")
        client.login(username="admin111")
        self.product3.delete()
        self.product4.delete()
        self.assertEqual(len(Product.objects.all()), 3)
