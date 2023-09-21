from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from bluemall.settings import AUTH_USER_MODEL as Person

# Create your models here.    
class Category(MPTTModel):
    name = models.CharField(
                            verbose_name=_('Category Name'),
                            help_text=_("Required and unique"),
                            max_length=255, 
                            unique=True
                        )
    slug = models.SlugField(
                            verbose_name=_('Category Safe URL'),
                            max_length=255,
                            allow_unicode=True,
                            unique=True
                            )
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                        )
    is_active = models.BooleanField(default=True)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name        = _('Category')
        verbose_name_plural = _('Categories')
        ordering            = ['-id']
    
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        return self.name




class ProductType(models.Model):
    """
    ProductType table will provide a list of the different types
    of products available for sale.
    """
    name = models.CharField(
        verbose_name=_('Product Type'),
        help_text=_('Required'),
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')
        
    def __str__(self):
        return self.name





class ProductSpecification(models.Model):
    """
    The product specification table contains product
    specification or features for the product types.
    """
    
    product_type = models.ForeignKey(ProductType, 
                                     related_name='product_type',
                                     on_delete=models.RESTRICT)
    name  = models.CharField(verbose_name=_('Name'),
                            help_text=_('Required'),
                            max_length=255
                            )
    
    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('Product Specifications')
    
    def __str__(self):
        return self.name





class Product(models.Model):
    #product information
    category     = models.ForeignKey(Category, 
                                    related_name='product_category', 
                                    on_delete=models.RESTRICT
                                    )
    product_type = models.ForeignKey(ProductType,
                                    on_delete=models.RESTRICT
                                    )
    author       = models.ForeignKey(Person,
                                     related_name='product_creator',
                                     on_delete=models.CASCADE
                                    )
    title       = models.CharField(verbose_name=_('title'), 
                                   help_text=_('Required'),
                                   max_length=255, 
                                   unique=True
                                   )
    slug        = models.SlugField(verbose_name=_('product safe url'), 
                                   max_length=255,
                                   allow_unicode=True, 
                                   unique=True
                                   )
    price       = models.DecimalField(
                                    verbose_name=_('regular price'),
                                    help_text=_('Maximum 999.99'),
                                    error_messages={
                                        "name": {
                                            "max_digits": _("The price must be between 0 and 999.99"),
                                        }
                                    },
                                    max_digits=5, 
                                    decimal_places=2
                                    )
    discount_price = models.DecimalField(
                                        verbose_name=_('discount price'),
                                        help_text=_('Maximum 999.99'),
                                        error_messages={
                                            "name": {
                                                "max_digits": _("The price must be between 0 and 999.99"),
                                            }
                                        },
                                        max_digits=5,
                                        decimal_places=2
                                    )
    description = models.TextField(verbose_name=_('description'), 
                                   help_text=_('Not Required'),
                                   blank=True
                                   )
    #product status
    is_active   = models.BooleanField(verbose_name=_('in stock'), 
                                      help_text=_('change if product is out of stock'), 
                                      default=True
                                      )
    created     = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated     = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)
    users_wishlist = models.ManyToManyField(Person, 
                                            related_name='user_wishlist',
                                            blank=True
                                            )
    
    class Meta:
        verbose_name        = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created']
    
    
    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title




class ProductSpecificationValue(models.Model):
    
    """
    product specification tables shows the specific features for a 
    particular table
    """
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=_('Value'),
                             help_text=_('product specification value (maximum of 255 words)'),
                             max_length=255,
                            )
    
    class Meta:
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('Product Specification Values')
    
    def __str__(self):
        return self.value





class ProductImage(models.Model):
    """
    Product image table
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image   = models.ImageField(verbose_name=_('image'),
                                help_text=_('Upload a product image'),
                                upload_to='images/products/',
                                default='images/default.png',
                                )
    alt_text   = models.CharField(verbose_name=_('alternative text'),
                                help_text=_('please add alternative text'),
                                max_length=255,
                                )
    is_feature = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at    = models.DateTimeField(auto_now=True, editable=False)
    
    
    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        
    def __str__(self):
        return self.alt_text