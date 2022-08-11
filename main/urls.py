from django.urls import path

from . import views
from .views import (ToDoListListView,
                    ItemListView,
                    ItemDetailView,
                    ItemCreateView,
                    ItemUpdateView,
                    ItemDeleteView
                    )

urlpatterns = [
    path("", views.home, name="home"),
    path("create_list/", views.create_list, name="create_list"),
    path("todo/", ToDoListListView.as_view(), name="todo"),
    path("show_items/<int:pk>", ItemListView.as_view(), name="items_list"),
    path("detail_item/<int:pk>", ItemDetailView.as_view(), name="item_detail"),
    path("create_item/<int:pk>",
         ItemCreateView.as_view(), name="item_create"),
    path("update_item/<int:pk>",
         ItemUpdateView.as_view(), name="item_update"),
    path("delete_item/<int:pk>",
         ItemDeleteView.as_view(), name="item_delete"),
]

'''
    path("edit_items/<int:id>", views.edit_items, name="edit_items"),
    path("list/<int:id>", views.show_list, name="show_list"),
    
'''
