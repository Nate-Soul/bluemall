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

app_name = 'payment'
urlpatterns = [
    path('', views.payment_options, name='payment_options'),
    path('delivery_options/', views.delivery_options, name='delivery_options'),
    path('update_basket_delivery/', views.update_basket_delivery, name='delivery_basket_update'),
    path('delivery_address/', views.delivery_address, name='delivery_address'),
    path('complete/', views.payment_complete, name='payment_complete'),
    path('successful/', views.payment_successful, name='payment_successfull'),
]