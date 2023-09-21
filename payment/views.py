import json

from django.utils.text import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from payment.models import DeliveryOptions
from account.models import Address
from orders.models import Order, OrderItem
from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest

# Create your views here.
@login_required
def delivery_options(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    context = {'delivery_options': delivery_options}
    return render(request, 'payment/delivery_options.html', context)



@login_required
def update_basket_delivery(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("delivery_option"))
        delivery_type   = DeliveryOptions.objects.get(id=delivery_option)
        
        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
            
    response = JsonResponse({
        "final_price": cart.get_final_price(),
        "delivery_fee": delivery_type.price
    })
    return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in session:
        messages.warning(request, "Please select a delivery option to continue")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    addresses = Address.objects.filter(customer_id=request.user.id).order_by('-default')
    
    if addresses:
        session = request.session
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].id),}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True
            
    context = {'addresses': addresses,}
    return render(request, 'payment/delivery_address.html', context)            



@login_required
def payment_options(request):
    if "address" not in request.session:
        messages.warning(request, "Please select an address to continue")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    if "purchase" in request.session and "address"  in request.session:
        delivery_option = DeliveryOptions.objects.get(id=int(request.session["purchase"]["delivery_id"]))
        address = Address.objects.get(customer=request.user, id=slugify(request.session["address"]["address_id"]))
    
    context = {'address': address,
               'delivery_option': delivery_option,
               }
    return render(request, 'payment/checkout.html', context)



@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    
    print(request.body)
    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id
    
    request_order = OrdersGetRequest(data)
    
    response = PPClient.client.execute(request_order)
    
    cart = Cart(request)
    
    order = Order.objects.create(
        user_id         = user_id,
        full_name       = response.result.purchase_units[0].shipping.name.full_name,
        email           = response.result.payer.email_address,
        address_1       = response.result.purchase_units[0].shipping.address.address_line_1,
        address_2       = response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code     = response.result.purchase_units[0].shipping.address.postal_code,
        country_code    = response.result.purchase_units[0].shipping.address.country_code,
        total_paid      = response.result.purchase_units[0].amount.value,
        order_key       = response.result.id,
        payment_option  = "paypal",
        billing_status  = True
    )
    
    order_id = order.pk
    
    for item in cart:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
        
    return JsonResponse("Payment Completed!", safe=False)



@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/order_placed.html')