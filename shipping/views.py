from django.shortcuts import render
from django.views import generic, View
from .models import Shipping


class ShippingList(generic.ListView):
    """ A view to render shipping.html page """
    model = Shipping
    queryset = Shipping.objects.filter(active=True)
    template_name = "shipping/shipping.html"
