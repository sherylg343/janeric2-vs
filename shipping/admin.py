from django.contrib import admin
from .models import Shipping
from django_summernote.admin import SummernoteModelAdmin


class ShippingAdmin(SummernoteModelAdmin):

    list_display = ('title', 'body', 'created_on', 'modified_on')
    summernote_fields = ('body',)

admin.site.register(Shipping, ShippingAdmin)
