import json

from django.urls import reverse
from rest_framework.test import APITestCase
from products.models import Product
from shopping_baskets.models import ShoppingBasket
from users.models import User


class ShoppingBasketCreateAPIViewTestCase(APITestCase):
    url = reverse('shopping_baskets:shopping-baskets-list')

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.user2 = User.objects.create_user('user2', 'user2@testsite.com', 'user2')

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

        self.shopping_basket1 = ShoppingBasket.objects.get(user=self.user1)
        self.shopping_basket1.products.add(self.product1, self.product2)

    def test_get_list_success_as_user(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        content = json.loads(response.content)[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('user'), self.user1.id)
        self.assertEqual(len(content.get('products')), 2)
        for item in zip(content.get('products'), list(self.shopping_basket1.products.all())):
            self.assertEqual(item[0].get('name'), item[1].name)
            self.assertEqual(item[0].get('description'), item[1].description)
            self.assertEqual(float(item[0].get('price')), float(item[1].price))
            self.assertEqual(item[0].get('category'), item[1].category)

    def test_get_list_fail_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


class ShoppingBasketDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.user2 = User.objects.create_user('user2', 'user2@testsite.com', 'user2')

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

        self.shopping_basket1 = ShoppingBasket.objects.get(user=self.user1)

        self.url_add_product = reverse(
            'shopping_baskets:shopping-baskets-add-products',
            kwargs={'pk': self.shopping_basket1.id}
        )
        self.url_get_basket = reverse(
            'shopping_baskets:shopping-baskets-detail',
            kwargs={'pk': self.shopping_basket1.id}
        )

        self.shopping_basket1.products.add(self.product1, self.product2)
        self.url_delete_product = reverse(
            'shopping_baskets:shopping-baskets-delete-product',
            kwargs={'pk': self.shopping_basket1.id, 'product_id': self.product1.id}
        )

    def tearDown(self):
        self.shopping_basket1.products.clear()

    def test_add_products_success_as_user(self):
        self.client.force_authenticate(self.user1)
        data = {
            'products': [self.product1.id],
        }
        response = self.client.put(self.url_add_product, data)
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertListEqual(content.get('products'), data['products'])

    def test_add_products_fail_as_another_user(self):
        self.client.force_authenticate(self.user2)
        data = {
            'products': [self.product1.id],
        }
        response = self.client.put(self.url_add_product, data)
        self.assertEqual(403, response.status_code)

    def test_add_products_fail_as_unauthorized(self):
        self.client.logout()
        data = {
            'products': [self.product1.id],
        }
        response = self.client.put(self.url_add_product, data)
        self.assertEqual(401, response.status_code)

    def test_delete_success_as_user(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(self.url_delete_product)
        self.assertEqual(204, response.status_code)

    def test_delete_fail_as_unauthorized(self):
        self.client.logout()
        response = self.client.delete(self.url_delete_product)
        self.assertEqual(401, response.status_code)

    def test_get_basket_success_as_user(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url_get_basket)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('user'), self.user1.id)
        self.assertEqual(len(content.get('products')), 2)
        for item in zip(content.get('products'), [self.product1, self.product2]):
            self.assertEqual(item[0].get('name'), item[1].name)
            self.assertEqual(item[0].get('description'), item[1].description)
            self.assertEqual(float(item[0].get('price')), item[1].price)
            self.assertEqual(item[0].get('category'), item[1].category)

    def test_get_basket_fail_as_another_user(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url_get_basket)
        self.assertEqual(403, response.status_code)

    def test_get_basket_fail_as_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url_get_basket)
        self.assertEqual(401, response.status_code)
