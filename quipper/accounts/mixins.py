from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class OwnedByUserMixin(UserPassesTestMixin):
    def test_func(self):
        """Check that the user owns this chirp"""
        return self.get_object().user == self.request.user


class AssignToUserMixin(LoginRequiredMixin):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddUserContextData(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class JsonResponseMixin(object):
    """Somewhat awkward as its not clear where to put utility 
    functions, but I like keeping them in accounts"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({"url_redirect": "/"}, status=200)
        return response
