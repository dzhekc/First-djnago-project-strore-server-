from http import HTTPStatus
from http.client import HTTPResponse
from itertools import product
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from unicodedata import category

from models import Product, ProductCategory


class ProductsViewTestCase(TestCase):
    fixtures = ['products.json','categories.json']

    def setUp(self):
        self.products = Product.objects.all()

    def _common_test(self,response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'],'clown')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))


    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:index',args=(category,))
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products.filter(category_id=category.id)))

        a = 1


# Create your tests here.
