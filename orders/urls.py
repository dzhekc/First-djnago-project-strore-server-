from django.contrib import admin
from django.urls import path,include
from django.conf import settings

from orders.views import OrderCreateView,SuccessView,CancelTemplateView,OrderListView

from orders.views import OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('create/',OrderCreateView.as_view(),name='order-create'),
    path('order-success/',SuccessView.as_view(),name='order-success'),
    path('order-cancel/',CancelTemplateView.as_view(),name='order-cancel'),
    path('',OrderListView.as_view(),name='orders'),
    path('order/<int:pk>/',OrderDetailView.as_view(),name='order-detail'),
]

