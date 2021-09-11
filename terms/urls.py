from django.urls import path
from . import views


urlpatterns = [
    path('', views.TermsList.as_view(), name='terms'),
]
