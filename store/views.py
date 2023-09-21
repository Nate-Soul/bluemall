from django.shortcuts import render, get_object_or_404

from .models import Category, Product


# Create your views here.
def home(request):
    products = Product.objects.prefetch_related('product_image').filter(is_active=True)
    return render(request, 'store/index.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product.html', {'product': product})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category).filter(is_active=True)
    return render(request, 'store/category.html', {'products': products,
                                                    'category': category
                                                    }
                  )
    
    