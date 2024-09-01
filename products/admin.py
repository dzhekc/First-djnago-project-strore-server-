from django.contrib import admin

# Register your models here.

from products.models import Product, ProductCategory,Basket


admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = ('image','name','description','price','quantity','category','stripe_product_price_id',)
    search_fields = ('name',)
    ordering = ('name',)

class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product','quantity')
    extra = 3