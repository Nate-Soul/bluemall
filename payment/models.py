from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class DeliveryOptions(models.Model):
    """
    Model for delivery/shipping options
    """
    
    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]
    
    name = models.CharField(verbose_name=_('Delivery Name'),
                            help_text=_('Required'),
                            max_length=255
                            )
    
    price = models.DecimalField(verbose_name=_('Delivery Fee'),
                                help_text=_('Maximum 999.99'),
                                error_messages={
                                    "name": {
                                        "max_length": _("The price must be between 0.00 and 999.99")
                                    }
                                },
                                max_digits=5,
                                decimal_places=2
                                )
    
    method = models.CharField(verbose_name=_('Delivery Method'),
                              help_text=_('Required'),
                              choices=DELIVERY_CHOICES,
                              max_length=255,
                              )
    timeframe = models.CharField(verbose_name=_('Delivery Timeframe'),
                                 help_text=_('Required'),
                                 max_length=255,
                                 )
    window    = models.CharField(verbose_name=_('Delivery Window'),
                                 help_text=_('Required'),
                                 max_length=255
                                 )
    order     = models.IntegerField(verbose_name=_('List Order'),
                                    help_text=_('Required'),
                                    default=0
                                    )
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Delivery Option')
        verbose_name_plural = _('Delivery Options')
        
    def __str__(self):
        return self.name
    


class PaymentOptions(models.Model):
    """
    Model for store payment options
    """
    name = models.CharField(verbose_name=_('Payment Name'),
                            help_text=_('Required'),
                            max_length=255,
                            )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Payment Option')
        verbose_name_plural = _('Payment Options')
        
    def __str__(self):
        return self.name
    