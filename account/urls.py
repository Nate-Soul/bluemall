"""bluemall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('registration-successful/', views.PasswordEmailConfirmView.as_view(), name='registration-success'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('reset/password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('password/reset/<slug:uidb64>/<slug:token>/', views.ConfirmResetPasswordView.as_view(), name='reset-password-confirm'),
    path('reset/password/email-confirmed/', views.PasswordEmailConfirmView.as_view(), name='reset-password-email-confirm'),
    path('reset/password/completed/', views.PasswordEmailConfirmView.as_view(), name='reset-password-complete'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.CustomUserLogoutView.as_view(), name='logout'),
    #user dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('orders/', views.user_orders_view, name='orders'),
    path('profile/edit/', views.user_profile_edit, name='profile-edit'),
    path('password/edit/', views.user_change_password, name='password-edit'),
    path('profile/delete/', views.user_delete, name='profile-delete'),
        #addresses
    path('addresses/', views.user_addresses, name='addresses'),
    path('addresses/<slug:id>/edit/', views.user_edit_address, name='edit_address'),
    path('addresses/<slug:id>/delete/', views.user_delete_address, name='delete_address'),
    path('addresses/<slug:id>/set_default/', views.user_set_default_address, name='set_default_address'),
        #wishlist
    path('wishlist/', views.user_wishlist, name='wishlists'),
    path('wishlist/<int:id>/add/', views.user_add_to_wishlist, name='add_to_wishlist'),
]