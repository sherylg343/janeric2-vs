from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShippingList.as_view(), name='shipping'),
]
