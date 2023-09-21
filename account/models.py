from email import contentmanager
import uuid
from django.contrib.auth.models import ( AbstractBaseUser,
                                        BaseUserManager, 
                                        PermissionsMixin
                                        )
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail

# Create your models here.
class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))
        
        return self.create_user(email, name, password, **other_fields)
    
    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('Email address is required'))
        
        email = self.normalize_email(email)
        user =  self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    #customer account info
    name            = models.CharField(max_length=150)
    email           = models.EmailField(_('email address'), unique=True)
    mobile          = models.CharField(max_length=20, blank=True)
    #user status
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    #custom
    objects = CustomAccountManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'
        unique_together = ('email', 'name')
        
    def __str__(self):
        return self.name
        
    def email_user(self, subject, message):
        send_mail(
            subject = subject,
            message = message,
            from_email = None,
            recipient_list = [self.email],
            fail_silently = False
        )


class Address(models.Model):
    id              = models.UUIDField(primary_key=True, 
                                       default=uuid.uuid4, 
                                       editable=False
                                       )
    #customer info
    customer        = models.ForeignKey(Customer, 
                                        verbose_name=_('Customer'),
                                        on_delete=models.CASCADE, 
                                        related_name='customer_address'
                                        )
    full_name       = models.CharField(_('Full Name'), max_length=200)
    phone           = models.CharField(_('Phone Number'), max_length=15)
    #delivery info
    address_line_1  = models.CharField(_('Address Line 1'), max_length=150)
    address_line_2  = models.CharField(_('Address Line 2'), max_length=150)
    postcode        = models.CharField(_('Post Code'), max_length=6)
    town            = models.CharField(_('City/Town'), max_length=150)
    state           = models.CharField(_('State/Province'), max_length=150)
    country         = CountryField(blank_label=_('Select Country'))
    notes           = models.TextField(_('Delivery Notes'), max_length=300)
    #delivery status
    default         = models.BooleanField(_('Default'), default=False)
    created_at      = models.DateTimeField(_('Created_at'), auto_now_add=True)
    updated_at      = models.DateTimeField(_('Updated_at'), auto_now=True)
    
    class Meta:
        verbose_name =        "Address"
        verbose_name_plural = "Addresses"
        
    def __str__(self):
        return "Address"