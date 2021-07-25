from django.shortcuts import render
from django.views import generic
from .models import Shipping


#def shipping(request):
#    """ A view to render shipping.html page """
#    return render(request, 'shipping/shipping.html')

class ShippingList(generic.ListView):
    """ A view to render shipping.html page """
    model = Shipping
    queryset = Shipping.objects.all()
    template_name = 'shipping.html'
