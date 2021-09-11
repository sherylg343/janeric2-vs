from django.shortcuts import render
from django.views import generic, View
from .models import Terms


class TermsList(generic.ListView):
    """ A view to render shipping.html page """
    model = Terms
    queryset = Terms.objects.filter(active=True)
    template_name = "terms/terms.html"
