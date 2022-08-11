from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import is_valid_path, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django import forms

from .models import ToDoList, Item
from .forms import CreateNewList

# ---------------------------------------------------------
# The first part demonstrates how to use function based views
# ---------------------------------------------------------


def home(response):
    return render(response, "main/home.html", {})


def create_list(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            name_cleaned = form.cleaned_data["name"]
            todo = ToDoList(name=name_cleaned, user=request.user)
            todo.save()
            messages.success(
                request, f'New List {name_cleaned} created.')
        else:
            messages.error(
                request, f'There was an error creating New List.')

        # return HttpResponseRedirect("/%i" % todo.id)
        return HttpResponseRedirect("/todo")
    else:
        form = CreateNewList()

    context = {'form': form,
               'title': "Create New List"
               }
    return render(request, "main/create_list.html", context)


# ---------------------------------------------------------
# The second part demonstrates how to use Class based views
# ---------------------------------------------------------


class ToDoListListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ToDoList
    # looks for <app>/<model>_<viewtype>.html ie main/todolist_list.html
    # passes object_list to the template

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    # pass title to the template
    def get_context_data(self, **kwargs):
        context = super(ToDoListListView, self).get_context_data(**kwargs)
        context['title'] = "Show User List"
        return context


class ItemListView(ListView):
    model = Item
    # looks for <app>/<model>_<viewtype>.html ie main/item_list.html
    # passes object_list to the template

    # filter the item list only for this todolist_id
    def get_queryset(self):
        return Item.objects.filter(todolist_id=self.kwargs['pk'])

    # get the name of the list and pass to the template
    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['list_name'] = ToDoList.objects.get(id=self.kwargs['pk'])
        context['list_id'] = self.kwargs['pk']
        context['title'] = "Show List Items"
        return context


class ItemDetailView(DetailView):
    model = Item

    # get the name of the list and pass to the template
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        item = Item.objects.get(id=self.kwargs['pk'])
        context['list_name'] = item.todolist.name
        return context


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Item

    fields = ['text', 'target_date', 'complete']

    # class Meta:
    #    widgets = {'target_date': DateInput()}

    def get_form(self):
        '''add date picker in forms'''
        form = super(ItemCreateView, self).get_form()
        form.fields['target_date'].widget = DateInput()
        return form

    def form_valid(self, form):
        form.instance.todolist_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['list_id'] = self.kwargs['pk']
        context['title'] = "Create Item"
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Item

    fields = ['text', 'target_date', 'complete']

    def get_form(self):
        '''add date picker in forms'''
        form = super(ItemUpdateView, self).get_form()
        form.fields['target_date'].widget = DateInput()
        return form

    def test_func(self):
        item = self.get_object()
        if self.request.user.id == item.todolist.user_id:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        item = Item.objects.get(id=self.kwargs['pk'])
        context['list_id'] = item.todolist_id
        context['title'] = "Update Item"
        return context


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item

    # item = Item.objects.get(id=pk)
    # success_url = f"show_items/{item.todolist_id}"

    # get the id of the list and pass to the template
    def get_context_data(self, **kwargs):
        context = super(ItemDeleteView, self).get_context_data(**kwargs)
        item = Item.objects.get(id=self.kwargs['pk'])
        context['list_id'] = item.todolist_id
        context['title'] = "Delete Item"
        return context

    def test_func(self):
        item = self.get_object()

        if self.request.user.id == item.todolist.user_id:
            return True
        return False

    # we want to get back to the previous page ie items_list view with
    # the given todolist_id (same as when we cancel)
    def get_success_url(self):
        return reverse('items_list', kwargs={'pk': self.object.todolist_id})
