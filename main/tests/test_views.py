from django.test import TestCase, Client, override_settings
from django.urls import reverse
from main.models import ToDoList, Item
import json


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.create_list_url = reverse('create_list')

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_create_list_GET(self):
        response = self.client.get(self.create_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_list.html')

    def test_create_list_GET(self):
        response = self.client.get(self.create_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_list.html')

    # Need to add more detailed tests ...
