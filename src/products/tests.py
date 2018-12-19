import json

from django.urls import reverse
from rest_framework.test import APITestCase

from products.models import Product
from users.models import User


class ProductCreateAPIViewTestCase(APITestCase):
    url = reverse('products:products-list')

    def setUp(self):
        self.user = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.superuser = User.objects.create_superuser('admin', 'admin@testsite.com', 'admin')

    def test_create_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        data = {
            'name': 'Product 1',
            'description': 'Product description 1',
            'price': 10.99
        }
        response = self.client.post(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(201, response.status_code)
        self.assertEqual(content.get('name'), data['name'])
        self.assertEqual(content.get('description'), data['description'])
        self.assertEqual(float(content.get('price')), data['price'])

    def test_create_fail_as_user(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Product 1',
            'description': 'Product description 1',
            'price': 10.99
        }
        response = self.client.post(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_get_list_success_as_user(self):
        self.client.force_authenticate(self.user)

        self.product1 = Product.objects.create(
            name='Product 1',
            description='Product description 1',
            price=10.99
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            description='Product description 2',
            price=2.50
        )
        self.product3 = Product.objects.create(
            name='Product 3',
            description='Product description 3',
            price=8.00
        )

        response = self.client.get(self.url)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(content), 3)
        for item in zip(content, [self.product1, self.product2, self.product3]):
            self.assertEqual(item[0].get('name'), item[1].name)
            self.assertEqual(item[0].get('description'), item[1].description)
            self.assertEqual(float(item[0].get('price')), item[1].price)

    def test_get_list_fail_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


class ProductDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.superuser = User.objects.create_superuser('admin', 'admin@testsite.com', 'admin')

        self.product1 = Product.objects.create(
            name='Product 1',
            description='Product description 1',
            price=10.99
        )
        self.url = reverse('products:products-detail', kwargs={'pk': self.product1.id})

    def test_update_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        data = {
            'name': 'Product 1 updated',
            'description': 'Product description 1',
            'price': 10.99
        }
        response = self.client.put(self.url, data)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('name'), data['name'])
        self.assertEqual(content.get('description'), data['description'])
        self.assertEqual(float(content.get('price')), data['price'])

    def test_update_fail_as_user(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Product 1 updated',
            'description': 'Product description 1',
            'price': 10.99
        }
        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_get_product_success_as_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('name'), self.product1.name)
        self.assertEqual(content.get('description'), self.product1.description)
        self.assertEqual(float(content.get('price')), self.product1.price)

    def test_delete_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_delete_fail_as_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_delete_fail_as_unauthorized(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(401, response.status_code)
