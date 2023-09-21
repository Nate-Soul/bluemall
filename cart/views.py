from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product

# Create your views here.
def cart(request):
    context = {'cart': Cart(request)}
    return render(request, 'cart/cart.html', context)



def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'add':
        product_id = int(request.POST.get('productId'))
        product_qty = abs(int(request.POST.get('productQty')))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        cart_items = cart.__len__()
        response = JsonResponse({
            'qty': cart_items,
        })
        return response
    
    
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'update':
        product_id = int(request.POST.get('productId'))
        product_qty = abs(int(request.POST.get('productQty')))
        cart.update(product=product_id, qty=product_qty)
        cart_items = cart.__len__()
        updated_price = cart.get_total_price(product_id)
        cart_sub = cart.get_sub_total()
        response = JsonResponse({
            'qty': cart_items,
            'total': updated_price,
            'sub_total': cart_sub,
        })
        return response
    
    

def cart_delete(request):
    cart = Cart(request)    
    if request.POST.get('action') == 'delete':
        product_id = int(request.POST.get('productId'))
        cart.delete(product=product_id)
        cart_items = cart.__len__()
        cart_sub_total = cart.get_sub_total()
        response = JsonResponse({
            'qty': cart_items,
            'sub_total': cart_sub_total,
        })
        return response