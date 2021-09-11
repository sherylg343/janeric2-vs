from django.contrib import admin
from .models import Terms
from django_summernote.admin import SummernoteModelAdmin


class TermsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'subtitle', 'body', 'created_on', 'modified_on')
    summernote_fields = ('body',)

admin.site.register(Terms, TermsAdmin)
