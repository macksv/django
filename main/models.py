from datetime import datetime
from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.


class ToDoList(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()
    target_date = models.DateField(null=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        # we used to return to the item_detail but now that we list all
        # items we now just go back to list_item_list
        # return reverse('item_detail', kwargs={'pk': self.pk})
        return reverse('items_list', kwargs={'pk': self.todolist_id})
