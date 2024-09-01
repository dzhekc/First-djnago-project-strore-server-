import stripe
import os
import sys
from django.db import models
from user.models import User
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=256,null = True,blank=True)
    category = models.ForeignKey(to=ProductCategory,on_delete=models.CASCADE)


    def __str__(self):
        return f"Товар {self.name} ценой {self.price}"

    def save(self, *args, **kwargs):
        if not self.stripe_product_price_id:
            stripe_obj = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_obj['id']
        super().save(*args, **kwargs)


    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name = self.name)
        stripe_product_price = stripe.Price.create(product = stripe_product['id'],unit_amount=round(self.price * 100),currency='RUB')
        return stripe_product_price

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_count(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []

        for basket in self:
            item = {'price':basket.product.stripe_product_price_id,'quantity':basket.quantity}
            line_items.append(item)

        return line_items

class Basket(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина пользователя {self.user.username}|кол-во в корзине {self.quantity}"

    def sum(self):
        return self.product.price * self.quantity

    def create_json(self):
        basket_item = {
            'name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.sum()),
        }
        return basket_item



