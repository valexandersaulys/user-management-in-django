from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from quips.models import Quip
from accounts.mixins import (
    OwnedByUserMixin,
    AssignToUserMixin,
    AddUserContextData,
    JsonResponseMixin,
)


class QuipListView(AddUserContextData, ListView):
    # quip_list.html
    model = Quip
    context_object_name = "quips"  # will get renamed in template
    # paginate_by = int   # if you want to
    # def get_queryset()   # can be overridden


class QuipDetailView(DetailView):
    # quip_detail.html
    model = Quip
    context_object_name = "quip"  # will get renamed in template


class QuipCreateView(JsonResponseMixin, AssignToUserMixin, CreateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")


class QuipUpdateView(OwnedByUserMixin, UpdateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")


class QuipDeleteView(OwnedByUserMixin, DeleteView):
    # GET: quip_confirm_delete.html, POST: delete and go to success url
    model = Quip
    success_url = reverse_lazy("quip_list")
