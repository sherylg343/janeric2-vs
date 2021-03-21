# From hacksoft.io/improve-your-tests-django-fakes-and-factories/
import factory
from faker import Faker
from factory import lazy_attribute

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Category'

    name = factory.Sequence(lambda n: 'Category{0}' .format(n))
    division = factory.Faker('word')


class Product_FamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Product_Family'

    name = factory.Sequence(lambda n: 'Product_Family{0}' .format(n))
    brand_name = factory.Faker('word')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Product'

    category = factory.SubFactory(CategoryFactory)
    product_family = factory.SubFactory(Product_FamilyFactory)
    name = factory.Sequence(lambda n: 'Test Product {0}' .format(n))
