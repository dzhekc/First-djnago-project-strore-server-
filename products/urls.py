
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from products.views import products,basket_add,basket_remove,ProductsListView

from django.views.decorators.cache import cache_page


app_name = 'products'
urlpatterns = [
    path('',ProductsListView.as_view(),name='index'),
    path('page/<int:page>/',ProductsListView.as_view(),name='paginator'),
    path('category/<int:category_id>',ProductsListView.as_view(),name='category'),
    path('baskets/add/<int:product_id>/', basket_add,name='basket_add'),
    path('baskets/remove/<int:baske_id>/',basket_remove, name='basket_remove')
]



