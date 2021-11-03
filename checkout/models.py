import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    class Meta:
        ordering = ('-order_date', )

    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    email = models.EmailField(
        max_length=254, null=False, blank=False)
    ship_full_name = models.CharField(
        max_length=50, null=True, blank=True)
    ship_comp_name = models.CharField(
        max_length=100, null=True, blank=True)
    ship_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    ship_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    ship_city = models.CharField(
        max_length=40, null=True, blank=True)
    ship_state = models.CharField(
        max_length=2, null=True, blank=True)
    ship_zipcode = models.CharField(
        max_length=10, null=True, blank=True)
    ship_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    bill_full_name = models.CharField(
        max_length=50, null=True, blank=True)
    bill_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    bill_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    bill_city = models.CharField(
        max_length=40, null=True, blank=True)
    bill_state = models.CharField(
        max_length=2, null=True, blank=True)
    bill_zipcode = models.CharField(
        max_length=10, null=True, blank=True)
    bill_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    order_date = models.DateTimeField(
        auto_now_add=True)
    shipping_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    ca_sales_tax = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(
        null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.shipping_cost = self.order_total * settings.STANDARD_SHIPPING_PERCENTAGE / 100
        self.grand_total = self.order_total + self.shipping_cost + self.ca_sales_tax
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.SKU} on order {self.order.order_number}'


class ShipFromAddress(models.Model):
    class Meta:
        ordering = ['shipper_reference_name', 'shipper_company_name', 'shipper_city']  
        verbose_name_plural = 'Ship From Addresses'

    shipper_reference_name = models.CharField(
        max_length=100, null=False, blank=False)
    shipper_company_name = models.CharField(
        max_length=100, null=False, blank=False)
    shipper_phone_number = models.CharField(
        max_length=20, null=False, blank=False)
    shipper_streetline1 = models.CharField(
        max_length=80, null=False, blank=False)
    shipper_streeline2 = models.CharField(
        max_length=80, null=True, blank=True)
    shipper_city = models.CharField(
        max_length=40, null=False, blank=False)
    shipper_state = models.CharField(
        max_length=2, null=False, blank=False)
    shipper_postal_code = models.CharField(
        max_length=10, null=False, blank=False)

    def __str__(self):
        return self.shipper_reference_name    


class ProductShippingData(models.Model):
    class Meta:
        ordering = ['product__active', 'product__category__division', 'product__category__name', 'product__product_family__name', 'product__product_size__name']  
        verbose_name_plural = 'Product Shipping Data'

    product = models.OneToOneField(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    product_pkg_weight_lb = models.DecimalField(
        max_digits=4, decimal_places=1, null=False, blank=False)
    shipper_address = models.ForeignKey(
         ShipFromAddress, null=False, blank=False, on_delete=models.CASCADE, related_name = 'shipper')
    
    def __str__(self):
        return self.product.name
