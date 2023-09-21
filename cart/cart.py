from payment.models import DeliveryOptions
from store.models import Product
from django.conf import settings
from decimal import Decimal

class Cart():
    
    """
        Cart class      
    """
    
    #initialize cart
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION)
        if settings.CART_SESSION not in request.session:
            cart = self.session[settings.CART_SESSION] = {}
        self.cart = cart
  
  
    
    #add to cart
    def add(self, product, qty):
        product_id = str(product.id)
        product_qty = int(qty)
        product_price = str(product.discount_price)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': product_price,
                                     'qty': product_qty,
                                    }
        self.save()
         
         
    
    #update cart item
    def update(self, product, qty):
        product_id = str(product)
        product_qty = qty
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
            self.cart[product_id]['total_price'] = str(Decimal(self.cart[product_id]['price']) * int(self.cart[product_id]['qty']))
            self.save()
    
    
    
    def __len__(self):
        '''
            get number of items in basket
        '''
        return sum(item['qty'] for item in self.cart.values())    
    
    
    
    def __iter__(self):
        '''
            iterate items in basket
        '''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = item['price']
            item['total_price'] = Decimal(item['price']) * int(item['qty'])
            yield item
    
    
    
    def get_total_price(self, product):
        return self.cart[str(product)]['total_price']
    
    
    
    def get_sub_total(self):
        return sum(Decimal(item['price']) * int(item['qty']) for item in self.cart.values())
    
    
    
    def get_delivery_fee(self):
        delivery_fee = 0.00
        if "purchase" in self.session:
            delivery_fee = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).price
        return delivery_fee
       
       
    def get_final_price(self):
        sub_total = self.get_sub_total()
        if sub_total == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(self.get_delivery_fee())
        
        total        = sub_total + shipping
        return total
        
    
    
    def delete(self, product):
        '''
            Delete item from cart
        '''
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
            
            
    def save(self):
        self.session.modified = True
        
        
        
    def clear(self):
        del self.session[settings.CART_SESSION]
        del self.session["purchase"]
        del self.session["address"]
        self.save()