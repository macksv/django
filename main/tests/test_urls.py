from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import (home, create_list,
                        ToDoListListView,
                        ItemListView,
                        ItemDetailView,
                        ItemCreateView,
                        ItemUpdateView,
                        ItemDeleteView)


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_create_list_url_resolves(self):
        url = reverse('create_list')
        self.assertEquals(resolve(url).func, create_list)

    def test_todo_url_resolves(self):
        url = reverse('todo')
        self.assertEquals(resolve(url).func.view_class, ToDoListListView)

    def test_items_list_url_resolves(self):
        url = reverse('items_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemListView)

    def test_items_detail_url_resolves(self):
        url = reverse('item_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemDetailView)

    def test_item_create_url_resolves(self):
        url = reverse('item_create', args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemCreateView)

    def test_item_update_url_resolves(self):
        url = reverse('item_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemUpdateView)

    def test_item_delete_url_resolves(self):
        url = reverse('item_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemDeleteView)
