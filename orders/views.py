#responses
from django.shortcuts import render
from django.http.response import JsonResponse
#models
from cart.cart import Cart
from .models import Order, OrderItem

# Create your views here.
def order_add_view(request):
    cart = Cart(request)
    if request.POST.get('action') == 'add':
        user_id     = request.user.id
        order_key   = request.POST.get('order_key')
        full_name   = request.POST.get('full_name')
        address_1   = request.POST.get('address_1')
        address_2   = request.POST.get('address_2')
        city        = request.POST.get('city')
        phone       = request.POST.get('phone')
        post_code   = request.POST.get('post_code')
        cart_total  = cart.get_sub_total()
        #check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=full_name, address_1=address_1,
                                 address_2=address_2, city=city, phone=phone, post_code=post_code,
                                 total_paid=cart_total, order_key=order_key)
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], 
                                         price=item['price'], quantity=item['qty'])
    response = JsonResponse({
        'success': 'Return true', 
    })
    return response
    
def user_orders(request):
    user = request.user.id
    orders = Order.objects.filter(user_id=user).filter(billing_status=True)
    return orders