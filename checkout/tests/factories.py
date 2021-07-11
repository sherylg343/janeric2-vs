import factory
from faker import Faker
from factory import lazy_attribute

from products import factories

fake = Faker()




active = factory.Faker("boolean", chance_of_getting_true=50)
quantity = factory.Faker("random_int", min=1, max=50)
#quantity = factory.LazyAttribute(lambda x: random.randrange(1, 30))