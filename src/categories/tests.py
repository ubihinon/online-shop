import json

from django.urls import reverse
from rest_framework.test import APITestCase

from categories.models import Category
from users.models import User


class CategoryCreateAPIViewTestCase(APITestCase):
    url = reverse('categories:categories-list')

    def setUp(self):
        self.user = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.superuser = User.objects.create_superuser('admin', 'admin@testsite.com', 'admin')

    def test_create_parent_category_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        data = {
            'name': 'Category 1',
        }
        response = self.client.post(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(201, response.status_code)
        self.assertEqual(content.get('name'), data['name'])

    def test_create_child_category_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        self.category1 = Category.objects.create(name='Parent cat')
        data = {
            'name': 'Category 1',
            'parent': self.category1.id
        }
        response = self.client.post(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(201, response.status_code)
        self.assertEqual(content.get('name'), data['name'])
        self.assertEqual(content.get('parent'), data['parent'])

    def test_create_fail_as_user(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Category 1',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_create_fail_as_unauthorized(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Category 1',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_get_list_success_as_user(self):
        self.client.force_authenticate(self.user)

        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.category3 = Category.objects.create(name='Category 3')

        response = self.client.get(self.url)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(content), 3)
        for item in zip(content, [self.category1, self.category2, self.category3]):
            self.assertEqual(item[0].get('name'), item[1].name)

    def test_get_list_fail_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


class CategoryDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user1', 'user1@testsite.com', 'user1')
        self.superuser = User.objects.create_superuser('admin', 'admin@testsite.com', 'admin')

        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2', parent=self.category1)
        self.category3 = Category.objects.create(name='Category 3')

        self.url = reverse('categories:categories-detail', kwargs={'pk': self.category2.id})

    def test_update_success_as_superuser(self):
        self.client.force_authenticate(self.superuser)
        data = {
            'name': 'Category 2 updated',
            'parent': self.category3.id
        }
        response = self.client.put(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('name'), data['name'])
        self.assertEqual(content.get('parent'), data['parent'])

    def test_update_fail_as_user(self):
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Category 2 updated',
            'parent': self.category1.id
        }
        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_get_category_success_as_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('name'), self.category2.name)
        self.assertEqual(content.get('parent'), self.category1.id)

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
