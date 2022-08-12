from django.test import SimpleTestCase
from main.forms import CreateNewList


class TestForms(SimpleTestCase):

    def test_create_new_list_valid(self):
        form = CreateNewList(data={'name': 'Test List'})
        self.assertTrue(form.is_valid())

    def test_create_new_list_no_data(self):
        form = CreateNewList(data={})
        self.assertFalse(form.is_valid())
