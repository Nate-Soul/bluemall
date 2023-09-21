from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import (LoginView,
                                       LogoutView, 
                                       PasswordResetView, 
                                       PasswordResetConfirmView,
                                       )
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from store.models import Product

from .token import account_activation_token
from .forms import (
                    UserAddressForm,
                    RegistrationForm, 
                    CustomUserLoginForm, 
                    ResetPasswordForm, 
                    ResetPasswordConfirmForm,
                    ChangePasswordForm,
                    ProfileEditForm
                    )
from bluemall.settings import AUTH_USER_MODEL as UserBase
from .models import Customer, Address
from orders.views import user_orders

# Create your views here.
'''
    ACCOUNTS:
    Register, Activate, Login, Reset password, Confirm password reset and logout views
'''
#register view
def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user =  registerForm.save(commit=False)
            user.name = registerForm.cleaned_data['name']
            user.email = registerForm.cleaned_data['email']
            user.password = make_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            #setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('account:registration-success')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

#activate email
def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except:
        raise IntegrityError("Seems you clicked on the wrong activation link")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html', {})


# login view
class SignInView(LoginView):
    form_class      = CustomUserLoginForm
    success_url     = reverse_lazy('account:dashboard')
    template_name   = 'account/login.html'
   
    def form_valid(self, form):
        messages.success(self.request, 'You\'re Logged in')
        return super().form_valid(form)




#reset password
class ResetPasswordView(PasswordResetView):
    template_name = 'account/password_reset/password_reset_form.html'
    success_url   = reverse_lazy('account:reset-password-email-confirm')
    email_template_name = 'account/password_reset/password_reset_email.html'
    form_class  = ResetPasswordForm





#password reset email confirm view
class PasswordEmailConfirmView(TemplateView):
    template_name = 'account/password_reset/reset_status.html'
    
    


#confirm password reset
class ConfirmResetPasswordView(PasswordResetConfirmView):
    template_name = 'account/password_reset/password_reset_confirm.html'
    success_url   = reverse_lazy('account:reset-password-complete')
    form_class  = ResetPasswordConfirmForm



# logout view
class CustomUserLogoutView(LogoutView):
    success_url = reverse_lazy('account:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'You\'re Logged out, login to continue.')
        return super().form_valid(form)


'''
    USER DASHBOARD:
    view dashboard, edit profile, edit orders and payments here
'''
# dashboard view
@login_required
def user_dashboard(request):
    return render(request, 'account/user/dashboard.html', {})

# edit profile
@login_required
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes were made to your profile')
            return redirect('account:profile-edit')
    else:
        form = ProfileEditForm(instance=user)
    context = {
        'form': form,
        'change_psw_form': ChangePasswordForm(user),
    }
    return render(request, 'account/user/profile_edit.html', context)

@login_required
def user_change_password(request):
    if request.method == 'POST':
        change_psw_form = ChangePasswordForm(request.user, data=request.POST)
        if change_psw_form.is_valid():
            change_psw_form.save()
            messages.success(request, 'Password for this account has been changed')
            return HttpResponseRedirect(reverse('account:profile-edit'))
        else:
            messages.error(request, 'Error encountered!')
            return HttpResponseRedirect(reverse('account:profile-edit'))
    
@login_required
def user_delete(request):
    current_user = UserBase.objects.get(user_name=request.user)
    current_user.is_active = False
    current_user.save()
    messages.success(request, 'Account deleted!')
    logout(request.user)
    return redirect('account:login')

#orders
@login_required
def user_orders_view(request):
    orders = user_orders(request)
    context = {
        'orders': orders,
    }
    return render(request, 'account/user/orders.html', context)

#addresses
@login_required
def user_addresses(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            messages.success(request, 'Address added')
            return redirect('account:addresses')
    else: 
        address_form = UserAddressForm()
    
    user = request.user.id
    addresses = Address.objects.filter(customer_id=user).order_by('-default')
    return render(request, 'account/user/addresses.html', {
        'addresses': addresses,
        'address_form': address_form,
    })

@login_required
def user_edit_address(request, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    if request.method == 'POST':
        address_edit_form = UserAddressForm(instance=address, data=request.POST)
        if address_edit_form.is_valid():
            address_edit_form.save()
            messages.success(request, 'Address edited successfully')
            next_page = request.META.get("HTTP_REFERER")
            if "delivery_address" in next_page:
                return redirect("payment:delivery_address")
            else:
                return redirect('account:addresses')
    else:
        address_edit_form = UserAddressForm(instance=address)
    context = {
        'address_edit_form': address_edit_form,
    }
    return render(request, 'account/user/address_edit.html', context)

@login_required
def user_delete_address(request, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, 'Address deleted')
    return redirect('account:addresses')

@login_required
def user_set_default_address(request, id):
    user = request.user
    Address.objects.filter(customer=user, default=True).update(default=False)
    address = Address.objects.filter(pk=id, customer=user)
    address.update(default=True)
    messages.success(request, 'An address was set as default')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def user_add_to_wishlist(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.warning(request, product.title+' has been removed from your wishlist')
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, product.title+' has been added to your wishlist')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def user_wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    context = {'wishlists': products}
    return render(request, 'account/user/wishlist.html', context)