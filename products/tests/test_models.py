from django.test import TestCase
from products.models import Category, Product_Family, Product


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="test category name", division="test division")

    def test_assert_is_instance(self):
        c = Category.objects.get(pk=1)
        self.assertTrue(isinstance(c, Category))

    def test_category_methods(self):
        c = Category.objects.get(pk=1)
        self.assertEqual(c.__str__(), c.name)
        self.assertEqual(c.get_name(), c.name)
        self.assertEqual(c.get_division(), c.division)


class Product_FamilyTest(TestCase):
    def setUp(self):
        self.product_family = Product_Family.objects.create(
            name="test pf name", brand_name="test brand name")

    def test_assert_is_instance(self):
        f = Product_Family.objects.get(pk=1)
        self.assertTrue(isinstance(f, Product_Family))

    def test_product_family_methods(self):
        f = Product_Family.objects.get(pk=1)
        self.assertEqual(f.__str__(), f.name)
        self.assertEqual(f.get_name(), f.name)
        self.assertEqual(f.get_brand_name(), f.brand_name)


class ProductTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="test product name")

    def test_assert_is_instance(self):
        p = Product.objects.get(pk=1)
        self.assertTrue(isinstance(p, Product))

    def test_product_method(self):
        p = Product.objects.get(pk=1)
        self.assertEqual(p.__str__(), p.name)
