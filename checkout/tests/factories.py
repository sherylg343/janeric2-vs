import factory
from faker import Faker
from factory import lazy_attribute

from products.tests.factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)

fake = Faker()





quantity = factory.Faker("random_int", min=1, max=50)
#quantity = factory.LazyAttribute(lambda x: random.randrange(1, 30))