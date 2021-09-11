from django.db import models

# Create your models here.
class Shipping(models.Model):
    class Meta:
        verbose_name_plural = 'Shipping'

    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80, blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
