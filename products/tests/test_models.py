from django.test import TestCase
from products.models import Category, Product_Family, Product
from django.utils import timezone


class CategoryTest(TestCase):

    def create_category(self, name="category test name", division="test division"):
        return Category.objects.create(name="category test name", division="test division", created_at=timezone.now())

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__unicode__(), c.name)
        self.assertEqual(c.__unicode__(), c.division)


class Product_FamilyTest(TestCase):

    def create_product_family(self, name="pf test name", brand_name="test brand name"):
        return Product_Family.objects.create(name="pf test name", division="test brand_name", created_at=timezone.now())

    def test_product_family_creation(self):
        f = self.create_product_family()
        self.assertTrue(isinstance(f, Product_Family))
        self.assertEqual(f.__unicode__(), f.name)
        self.assertEqual(f.__unicode__(), f.brand_name)


class ProductTest(TestCase):

    def create_product(self, name="product test name"):
        return Product.objects.create(
            name="product test name", created_at=timezone.now())

    def test_product_creation(self):
        p = self.create_product()
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(p.__unicode__(), p.name)
