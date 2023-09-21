from django.contrib.auth.forms import ( AuthenticationForm, 
                                        PasswordResetForm, 
                                        SetPasswordForm, 
                                        PasswordChangeForm,
                                       )
from django import forms

from .models import Address, Customer
from django_countries.fields import Countries

#create your forms here
class RegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Your Name',
                                min_length=2,
                                max_length=50,
                                help_text='Required',
                                error_messages={'required': 'Name is required'},
                                widget=forms.TextInput({
                                    'placeholder': 'example John',
                                    'class': 'form-control',
                                })
                            )
    email = forms.EmailField(label='Enter email address',
                                max_length=100,
                                help_text='Required',
                                error_messages={'required': 'email is required'},
                                widget=forms.EmailInput({
                                    'placeholder': 'james@example.com',
                                    'class': 'form-control',
                                })
                            )
    password = forms.CharField(label='Enter password',
                                help_text='Required',
                                error_messages={'required': 'password is required'},
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter password',
                                    'class': 'form-control',
                                })
                            )
    password2 = forms.CharField(label='Confirm password',
                                help_text='Required',
                                error_messages={'required': 'password2 is required'},
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter password',
                                    'class': 'form-control',
                                })
                            )
    class Meta:
        model = Customer
        fields = ('name', 'email', 'password', 'password2')
        
    
    def clean_user_name(self):
        username = self.cleaned_data['name'].lower()
        r = Customer.objects.filter(user_name=username)
        if r.count():
            raise forms.ValidationError("Username already taken!")
        return username
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match!")
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email


#custom login form class
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email address',
                                widget=forms.EmailInput({
                                    'placeholder': 'james@example.com',
                                    'class': 'form-control',
                                })
                            )
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter password',
                                    'class': 'form-control',
                                })
                            )


class ProfileEditForm(forms.ModelForm):
    name   = forms.CharField(max_length=150,
                             label='Name',
                             widget=forms.TextInput({
                                 'class': 'form-control',
                                 'placeholder': 'Your name e.g John'
                             }))
    email  = forms.EmailField(label='Email Address',
                              max_length=100,
                              help_text='Not editable',
                              widget=forms.EmailInput({
                                  'class': 'form-control',
                                  'placeholder': 'Your Email',
                                  'disabled': 'disabled'
                              }))
    mobile = forms.CharField(label='Phone Number',
                             max_length=20,
                             widget=forms.TextInput({
                                 'class': 'form-control',
                                 'placeholder': 'Mobile Phone Number'
                             }))
    
    class Meta:
        model = Customer
        fields = ('name', 'email', 'mobile')

#user address form class
class UserAddressForm(forms.ModelForm):
    
    full_name = forms.CharField(label='Full Name',
                                 max_length=200,
                                 widget=forms.TextInput({
                                     'placeholder': 'Your Full Name',
                                     'class': 'form-control',
                                 }))
    
    phone    = forms.CharField(max_length=15,
                               label='Mobile Phone',
                               widget=forms.TextInput({
                                   'placeholder': 'Enter mobile phone number',
                                   'class': 'form-control',
                               }))
    
    address_line_1 = forms.CharField(max_length=100,
                               label='Address Line 1',
                               widget=forms.TextInput({
                                   'placeholder': 'Enter street address',
                                   'class': 'form-control',
                               }))
    
    address_line_2 = forms.CharField(max_length=100,
                               label='Address Line 2',
                               widget=forms.TextInput({
                                   'placeholder': 'Enter suite/apartment address',
                                   'class': 'form-control',
                               }))
    
    postcode = forms.CharField(max_length=6, label='Post Code', 
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter post code',
                               }))
    
    town = forms.CharField(max_length=100,
                               label='City/Town',
                               widget=forms.TextInput({
                                   'placeholder': 'Enter City or Town',
                                   'class': 'form-control',
                               }))
    
    state = forms.CharField(max_length=100,
                               label='Province/State',
                               widget=forms.TextInput({
                                   'placeholder': 'Enter state or province',
                                   'class': 'form-control',
                               }))
    
    country = forms.ChoiceField(choices=Countries,
                                label='Country',
                                widget=forms.Select({
                                   'class': 'form-select',
                               }))
    
    notes  = forms.CharField(label='Delivery Instructions',
                             max_length=255,
                             widget=forms.Textarea({
                                 'class': 'form-control',
                                 'rows': '2',
                                 'placeholder': 'Short Delivery Instruction here'
                             }))
    
    class Meta:
        model = Address
        fields = ('full_name', 'phone', 'address_line_1', 'address_line_2', 
                  'postcode', 'town', 'state', 'country', 'notes')
        


class ResetPasswordForm(PasswordResetForm):
    
    """
    class for user password reset form
    """
    
    email = forms.EmailField(label='Email address',
                             max_length=254, 
                             widget=forms.EmailInput({
                                    'placeholder': 'james@example.com',
                                    'class': 'form-control',
                                })
                            )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not Customer.objects.filter(email=email):
            raise forms.ValidationError("Email doesn't exist on our database, please check the email and try again.")
        return email



class ResetPasswordConfirmForm(SetPasswordForm):
    """
    reset password confirm form
    """
    new_password1 = forms.CharField(label='New Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter New password',
                                    'class': 'form-control',
                                })
                            )
    
    new_password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Confirm password',
                                    'class': 'form-control',
                                })
                            )



class ChangePasswordForm(PasswordChangeForm):
    """_summary_

    Args:
        PasswordChangeForm (_type_): _for users to change password_
    """
    old_password = forms.CharField(label='Old Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter New password',
                                    'class': 'form-control',
                                })
                            )
    
    new_password1 = forms.CharField(label='New Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Enter New password',
                                    'class': 'form-control',
                                })
                            )
    
    new_password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput({
                                    'placeholder': 'Confirm password',
                                    'class': 'form-control',
                                })
                            )