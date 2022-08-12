from django.test import TestCase
from main.models import ToDoList, Item
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="User1", password="bar",
                                             email="user1@x.com")
        self.my_list = ToDoList(
            name="My List",
            user=self.user
        )
        self.my_list.save()

        self.my_item1 = Item(text="Fix the roof", complete=True,
                             todolist=self.my_list)

        self.my_item2 = Item(text="Mow the lawn", complete=True,
                             todolist=self.my_list)

        self.my_item1.save()
        self.my_item2.save()

    def test_todolist_fk_user(self):
        my_list = self.my_list
        # print(my_list.user.todolist_set.filter(
        #    name="My List").first())
        my_list_username = my_list.user.username
        my_list_email = my_list.user.email
        self.assertEquals(my_list_username, "User1")
        self.assertEquals(my_list_email, "user1@x.com")

    def test_items_fk_todolist(self):
        my_item1 = self.my_item1
        my_item2 = self.my_item2
        my_list = self.my_list

        my_item1_list_name = my_item1.todolist.name
        my_item2_list_name = my_item1.todolist.name

        self.assertEquals(my_item1_list_name, "My List")
        self.assertEquals(my_item2_list_name, my_list.name)

    def test_todolist_item_cnt(self):
        my_list = self.my_list
        self.assertEquals(my_list.item_set.all().count(), 2)
