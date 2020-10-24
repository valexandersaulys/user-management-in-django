from django.views.generic import TemplateView

from accounts.mixins import AddUserContextData


class UserDetailView(AddUserContextData, TemplateView):
    template_name = "registration/user_detail.html"
