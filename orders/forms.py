from django import forms
from .models import Order


#create your forms here
class OrderForm(forms.ModelForm):
    """Form definition for Order."""
    full_name   = forms.CharField(max_length=100,
                                  label='Full Name',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Your Full Name'
                                  }))
    address_1   = forms.CharField(max_length=250,
                                  label='Address 1',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Address Road/Street/Close'
                                  }))
    address_2   = forms.CharField(max_length=250,
                                  label='Address 2',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Address Floor/Suite'
                                  }))
    city        = forms.CharField(max_length=50,
                                  label='City',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'City of Residence'
                                  }))
    phone       = forms.CharField(max_length=20,
                                  label='Mobile',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Your Mobile Phone'
                                  }))
    post_code   = forms.CharField(max_length=15,
                                  label='Post Code',
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Post Code'
                                  }))
    

    class Meta:
        """Meta definition for Orderform."""

        model = Order
        fields = ('full_name', 'address_1', 'address_2', 'city', 
                  'phone', 'post_code',)