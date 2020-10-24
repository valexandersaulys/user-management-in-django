# Account Management in Django

One of the key advantages of building software projects in Django is
leveraging a lot of the built-in scaffolding to move fast without
breaking things.

Amongst these is the user management tools django provides.

Unlike more minimalist frameworks like [Flash]() or even other
"batteries-included" like [Ruby-on-Rails](), Django can handle all
your user management for you within built-in tools.

Django doesn't provide quite everything for you, but it does provide a lot:

  * sign-in/sign-out functionality
  
  * protecting views and data from unauthorized or unathenticated
    users

  * password changes

  * emailed password resets

What it doesn't provide are user sign-up forms. It also makes it hard
to change the default user, instead making you extend that out.

But all of this is very powerful. You no longer have to spend hours
getting user management down right but can instead focus on building
your application and providing value with your software.

However, too get this functionality you'll have to use Django's class based
views.


## Class Based Views

Let's start with function based views -- where everybody first learns
Django. 

Function based views, or FBVs for short, have a straight forward
logic. Your request hits the function, it gets processed through a
series of if-else type statements, and it produces a response.

The problem is as your project gets more complicated. You'll need to
start adding lots of boiler plate to handle common tasks like
permissioning and validation.

"No problem," you might think, "I'll just write function decorators."

Indeed, Django offers a lot of these. But as your application gets
more and more complex, you'll likely still be writing redundant
code to handle what context gets passed to a rendered page or to query
a specific route for a specific object in your database. 

Django alleviates a lot of this with Class Based Views.

Class Based Views (CBVs) take a bit more to wrap your head around. The
logic is no longer straight forward. Instead, a request will pass
through a series of functions within an object before the response.

This has the added benefit of separating concerns within your
response. You can have one function handle form validation and another
model querying. Then, you can subclass these objects as a sort of
"template."

Django does precisely this under the hood. You write your CBVs
subclassing these generic classes but specify certain variables. The
object's functions know to look for those variables. So long as you
know the expected behaviour, you can save yourself a lot of time and
effort.

Knowing this is key to knowing how the default user management works
in Django.

Let's use an example to get familiar.


## The App

Let's think of a dead simple Twitter clone called Quipper.

We'll need users who make quips (i.e. tweets). These can be then be
seen by each user on a timeline. We'll let each user delete and edit
their own quips but not others.

I'm going to assume familiarity with starting a basic django project
with virtualenv at this point.

The project will be generated as follows:

  * quipper -- root level project
    * `quips`
    * `accounts`  -- more on this later

Then we'll create our very basic model:

```python
from django.db import models
from django.contrib.auth.models import User


class Quip(models.Model):
    # pk => primary key will be automatic
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = models.CharField(max_length=360)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "<%s: %s>" % (self.user, self.content)

    class Meta:
        ordering = ["-created_at"]
```

Next, we'll add in some basic views to start:

```python
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from quips.models import Quip


class QuipDetailView(DetailView):
    # quip_detail.html
    model = Quip
    context_object_name = "quip"  # will get renamed in template


class QuipCreateView(CreateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")


class QuipUpdateView(UpdateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")


class QuipDeleteView(DeleteView):
    # GET: quip_confirm_delete.html, POST: delete and go to success url
    model = Quip
    success_url = reverse_lazy("quip_list")
```

And then the urls:

```python
from django.urls import path, include

from quips.views import *

urlpatterns = [
    # will redirect to login view otherwise
    path("", QuipListView.as_view(), name="quip_list"),
    path("c/<int:pk>", QuipDetailView.as_view(), name="quip_detail"),
    path("c/create_quip/", QuipCreateView.as_view(), name="quip_create"),
    path("c/update_quip/<int:pk>", QuipUpdateView.as_view(), name="quip_update"),
    path("c/delete_quip/<int:pk>", QuipDeleteView.as_view(), name="quip_delete"),
]
```

Starting with these you'll notice very little code is written. This
can be quite strange if you're used to writing function based views
such as in Flask. Each of these CBVs does a lot of work on its own
and hides it from you to produce cleaner reading code.

If you take `DetailView`, we can provide as little as just the `model`
variable and it would still work. I added the `context_object_name`
for readability sake in the template (defaults to `{{ object
}}`). `DetailView` will find the correct object by primary key `pk`
passed in the url. It then passes that as the string in
`context_object_name` to the template at 
`templates/<app-name>/<model-name-in-lowercase>_detail.html` for
rendering.

This may sound like a lot -- there's a crib sheet at the end to help
you remember the pertinent details -- but once you grok it you can
move very fast.

The equivalent FBV would have a lot more involved. You'd have to write
code that looked for the specific object, looked for the specific
template, and added that object for the template

But what if we wanted more sophisticated object look-ups? That's where
mixins come in.


## Mixins

To start, there's two built-in mixins in Django: `UserPassesTestMixin`
and `LoginRequiredMixin`.

`UserPassesTestMixin` added a `test_func` function that is checked at
render time. If it returns `False`, a 403 (forbidden) is returned to
the user. This is usually reserved for
permissioning. `LoginRequiredMixin` is self-explanatory. 

But we can get more complex.

Python is an object oriented language and provides for inheritance. It
makes no distinction between mixins and classes;  the API to create
them is the same. Inheritance reads left-to-right: overloaded
functions are read from the leftmost object and then proceed to the
right most if `super()` is called.

We can use those facts to start writing our own mixins to add
functionality to our CBVs.

Let's add user contextual data to our quips. We'll use
`LoginRequiredMixin` as a base so we can expect a `self.request.user`
object. Then we'll overwrite the `form_valid(self, form)` function
that all editing views use. Before we complete a form validation,
we'll attach the currently logged in user as our user.

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class AssignToUserMixin(LoginRequiredMixin):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
```

Now we can add this back to our `QuipCreateView` remembering our
left-to-right inheritance.

```python
class QuipCreateView(AssignToUserMixin, CreateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")
```

Remembering what functions a particular CBV uses can be difficult to
remember. [The Django documentation doesn't help either]() as each CBV
is technically composed of multiple mixins/objects so you'll need to
click quite deep to see what gets called. Thankfully I built a cheat
sheet to help you with the important stuff. You can scroll to the end
to find it.

We can quickly build a number of Mixins to help us figure out some
basics involved. We'll throw in a mixin to check for ajax requests too
in case we want to go that direction.

Django encourages separation of concerns for mixins so we'll put these
under a separate `accounts/mixins.py`

```python
# accounts/mixins.py
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
```

And we'll go back and add these in as appropriate to our CBVs

```
# quips/views.py
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
```



## User Management CBVs

This is where the magic comes in.

Django not only has built-in CBVs but it also has built-in routes for
common user actions. These include:

  * login
  * logout
  * password changing
  * password resets over email


```python
# accounts/urls.py
from django.urls import path, include

from accounts.views import *


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", UserDetailView.as_view(), name="user_profile"),
]
```

