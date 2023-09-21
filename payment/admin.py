from django.contrib import admin

from .models import DeliveryOptions, PaymentOptions

# Register your models here.
admin.site.register(DeliveryOptions)
admin.site.register(PaymentOptions)
