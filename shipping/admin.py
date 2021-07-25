from django.contrib import admin
from .models import Shipping
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Shipping)
class ShippingAdmin(SummernoteModelAdmin):

    list_display = ('title', 'body', 'created_on', 'modified_on')
    summernote_fields = ('body',)
