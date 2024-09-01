from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from products.models import Product,ProductCategory,Basket
from unicodedata import category
from user.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

# Create your views here.

#функции = контроллеры = вьюхи



class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'clown'
        return context

class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        query_set = super().get_queryset().order_by('id')
        category_id = self.kwargs.get('category_id')
        if category_id:
            print(query_set.filter(category_id=category_id))
            return query_set.filter(category_id=category_id)
        else:
            return query_set




# def index(requests):
#     context = {
#         'title' : 'Test Title',
#         'username' : 'valeriy',
#         'is_promotion' : False,
#     }
#     return render(requests,'products/index.html',context=context)



def products(requests, category_id=None, page_number=1):
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    contex = {
        'title' : 'Store-каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }
    return render(requests,'products/products.html',context=contex)





@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user,product=product)
    print(baskets)

    if not baskets.exists():
        Basket.objects.create(user=request.user,product=product,quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_remove(request, baske_id):
    basket = Basket.objects.get(id=baske_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])