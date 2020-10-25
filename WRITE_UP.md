Guide to using CBVs — how to start w/them and why

  * why fbvs don’t cut it — violates DRY and creates very long functions for checking 
  * the basic cbvs — TemplateView, DetailView, etc 
  * leveraging editing cbvs 

Leveraging built in user management in Django 

  * the auto URLs 
  * the associated CBVs to those URLs
  * the most basic templates you could create for it 

The available Mixins and how to add Mixins 

  * LoginRequired and TestFunction 
  * some simple ones I wrote to help 

All built in classes and which mixins they pull on

  * sort of a cheat sheet — may even be worth putting in a static page for this 


_______________________________________________-


# Guide to Using Class Based Views

Django's unique class based views (CBV) system for creating views is
often mistunderstood. If properly used, it can speed up development
time while creating readable code that alleviates much technical
debt. 

Web frameworks mostly come in two flavors: micro and
"batteries-included"

Microframeworks like Flask and ExpressJS don't include anything. They
assume you'll build out everything.

"Batteries-included" frameworks like Laravel and Ruby-on-Rails include
almost everything you'd need. They often have an ORM for mapping
objects to databases, handling complex middleware, and so on.

Django falls in that latter category.

Django is unusually flexible for a "batteries-included" web
framework. It allows you to write functions or classes for views.

Most beginners will opt for function based views as they're easier to 
reason about. Your request comes into the function, gets processed,
then gets returned.

Class based views (CBVs) are far more gnarly. It's not clear on first
glance what your request does or where it goes. But understanding this
will massively improve productivity: you'll stop writing redundant
code (think
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)) and
be able to leverage a lot of pre-built code. This lets you write
faster and keeps your code far more readable, limiting technical debt
in the future.

The catch is that you have to grok CBVs.


## Why Function Based Views don't cut it

Function Based Views (FBVs) are the first way you'll probably learn to
write django views.

Requests come in as an object, they get processed, a response gets
made, typically in the form of a rendered template.

```python
def my_cool_view(request):
    # ... some processing logic
    return render(request, "my_cool_view_template.html", context)
```

They do work well but where things get complicated is as you build
your views.

The first stumbling block is going to be protecting views from
unauthenticated users. You'll discover the
`django.contrib.auth.decorators.login_required` decorator and attach
is the top of a function, simple enough.

```python
@login_required
def my_cool_view(request):
    # alternatively you could use `if request.user.is_authenticated: ...`
    # ... some processing logic
    return render(request, "my_cool_view_template.html", context)
```

But what if you want to block off a page to only users who own it?

Now you can build in the logic via an if-else statement within the
FBV. But this muddles logic as you're combining the processing of a
page with authentication checking.

```python
@login_required
def my_cool_view(request):
    if my_object.user == request.user:
        # ... some processing logic
        return render(request, "my_cool_view_template.html", context)
    return HttpResponseForbidden()  # from django.http
```


This also crops up if you're trying to handle multiple types of
requests to a given route. You'll need to start adding checking with
if-else statements within the function. Again, the logic is being
muddled as your one function is doing a lot of work here.

```python
@login_required
def my_cool_view(request):
    if request.method == 'GET':
        if my_object.user == request.user:
            # ... some processing logic
            return render(request, "my_cool_view_template.html",context)
    elif request.method == 'POST':
        if my_object.user == request.user:
            # ... different processing logic
            return redirect( "detail-view", pk = obj.pk)
    return HttpResponseForbidden()  
```

As this goes on, the function will become more and more difficult to
read. You could add lots of comments but you'll also find yourself
rewriting code like getting a particular obejct out of the
database.

Class based views help alleviate this.

Check out the following code which condenses everything from teh prior
FBVs:

```python
class MyCoolView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request):
        # some process logic
        return render(request, "my_cool_view_template.html",context)

    def post(self, request):
        # ... different processing logic
        return redirect( "detail-view", pk = self.obj.pk)

    def test_func(self):
        return self.get_obejct().user == self.request.user

    def get_object(self):
        # get the object out of database -- more on this later
        return obj
```

This looks much better. We separated out the concerns here so the
`get` and `post` requests are handled separately. We pull in
`UserPassesTestMixin` to open up `test_func` to check if the user owns
the object in question. Lastly, we separate out the logic to get the
object out of database so that we can use it in both our `get` and
`post` functions  and avoid rewriting the code that twice.

This only touches the beginning of class based views. Django includes
a number of built-in mixins and generic objects to massively speed up
writing applications. Once you get the hang of using them, you'll
increase your coding skills helping you get a full application up much
quicker.

Let's dig in.

## The Skeleton of a CBV

We'll need to start with some background on Python's intricacies in
inheritance. 

Class based views in Django leverage [mixins](). These is Python's
term for interfaces and is how Python handles multiple inheritance.

There's a lot to digest here and Python's way of handling multiple
inheritance is a bit controversial. But for our purposes, you need to
remember that inheritance overloads from the left-to-right.

Suppose we have an object with basic function foo. We then write
another object with the same foo function. In a third object, we
inherit from both and call foo. What happens?

```python
class obj1(object):
    def foo(self):
        print("foo from obj1")


class obj2(object):
    def foo(self):
        print("foo from obj2")


class obj3(obj1, obj2):
    def __init__(self):
        pass


my_cool_object = obj3()
my_cool_object.foo()
```

The answer completely depends on the order of classes in `obj3`. If we
include `obj1` first, it will be called.

```shell
$ python3 examples.py 
foo from obj1
```

But if we swap the order, we'll get the other `foo` function from
`obj2` instead.

```python
# ...

class obj3(obj2, obj1):
    def __init__(self):
        pass

my_cool_object = obj3()
my_cool_object.foo()
# >>> "foo from obj2
```

What if we start to call a the parent class function using `super()`?
This is where mixins come into play.

Python is an interpreted language and doesn't check if there is the
corresponding function in the parent class ahead of time. It will only
check on evaluation. This means we can write `obj2` to call a super
function that doesn't exist.

```python
class obj1(object):
    def foo(self):
        print("foo from obj1")


class obj2(object):
    def foo(self):
        print("foo from obj2")
        super().foo()  # NEW ADDITION


class obj3(obj2, obj1):
    def __init__(self):
        pass


my_cool_object = obj3()
my_cool_object.foo()
```

What's going on here?

`obj2` calls the parent class' `foo` function. It's own parent class
doesn't have one but the parent class of `obj3` does and will call the
next parent class in inheritance -- which is `obj1`.

```shell
$ python3 examples.py 
foo from obj2
foo from obj1
```

The functions are being read left to right and the right most object
is the "most senior" parent class in the call chain.

Note that attempting to subclass `obj2` directly and call `foo` will
result in an error being raised.

```python
# ...
my_cool_object = obj2()
my_cool_object.foo()

'''
$ python3 examples.py 
foo from obj2
Traceback (most recent call last):
  File "examples.py", line 18, in <module>
    my_cool_object.foo()
  File "examples.py", line 9, in foo
    super().foo()
AttributeError: 'super' object has no attribute 'foo'
'''

This is key to understanding CBVs. Django creates a lot of mixin
"primitives" that do very specific functions but are useless on their
own.

The lazy evaluation also means that these "primitive" mixins can rely
on a constant that doesn't yet exist but be expected in the subclass.

```python
class obj1(object):
    def foo(self):
        print("foo from %s" % self.my_subclassed_constant)


class obj2(obj1):
    my_subclassed_constant = "obj2"


my_cool_object = obj2()
my_cool_object.foo()
# >>> foo from obj2
```

This is all somewhat expected for those coming from backgrounds like
Java. Python makes it somewhat difficult with no distinction being
made between an interface (the more common term for a mixin) and an
object. It simply assumes "everybody is an adult" and will know the
difference when coding.

This all said, you'll rarely be touching primitive mixins within
Django. Instead, you'll be leveraging the almost built out CBVs 
and subclassing those. That's where the magic of Django's CBVs lies.

With that said, let's look at the first CBVs available.



## Basic CBVs -- `TemplateView`, `DetailView`, `ListView`

Under `django.views.generic` lie the first three CBVs we'll be looking
at:

  * [`django.views.generic.TemplateView`](
  https://docs.djangoproject.com/en/3.1/ref/class-based-views/base/#templateview)
    
  * [`django.views.generic.DetailView`](
    https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#detailview)
    
  * [`django.views.generic.ListView`](
    https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview)
    
`TemplateView` is the most straightforward. Provide a `template_name`
and insert into urls. At that url, it will return a rendered
template. Simple enough.

```python
# views.py
from django.views.generic import ListView, DetailView, TemplateView

class MyTemplateview(TemplateView):
    # note this resolves as "templates/<app-name>/my_template_name.html"
    template_name = "my_template_name.html"  
```

```python
# urls.py
from django.urls import path, include

from .views import *

urlpatterns = [
    path("", MyTemplateView.as_view(), name="my-template-view"),
]
```

But what if we want to add context? that's simple
enough. `TemplateView` uses the
[`ContextMixin`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin)
to provide two ways of adding extra context. We can pass a dictionary
to the keyword `extra_context` or override `def get_context_data(self,
**kwargs)`.

```python
# METHOD 1: passing an optional dictionary to `extra_context`
# views.py
from django.views.generic import ListView, DetailView, TemplateView

class MyTemplateview(TemplateView):
    # note this resolves as "templates/<app-name>/my_template_name.html"
    template_name = "my_template_name.html"
    extra_context = {"more_data": "look so more information"}
```

```python
# METHOD 2: overriding `def get_context_data(self, **kwargs))`
# views.py
from django.views.generic import ListView, DetailView, TemplateView

class MyTemplateview(TemplateView):
    # note this resolves as "templates/<app-name>/my_template_name.html"
    template_name = "my_template_name.html"

   def get_context_data(self, **kwargs):
       '''should return a dictionary'''
       context = super().get_context_data(**kwargs)
       context["more_data"] = "look some more information"
       return context
```

In both cases we can call `{{ more_data }}` within our rendered
template `my_template_name.html`. 

Notice the separation of concerns here. We have one function dedicated
to getting extra context for our template. That improves readability
as we only have to look at that function to figure out what context is
getting passed to the template.

Also note that, in the second example, we're calling `super()`. This
calls the parent class' `get_context_data`, which is preprocessing
other context data. This will be important later on when we're dealing
with editing classes.

Let's take a look at `DetailView` next.

```python
# views.py
from django.views.generic import ListView, DetailView, TemplateView

from .models import Quip

class QuipDetailView(DetailView):
    model = Quip
```

```python
# urls.py
from django.urls import path, include

from quips.views import *

urlpatterns = [
    path("c/<int:pk>", QuipDetailView.as_view(), name="quip_detail"),
]
```

This looks incomplete at first glance. We only added added a `model`
variable our CBV. What's going on?

`DetailView` handles all the logic of finding an object and rendering
the template with it correctly. It even has a default template to look
for: `<model-name>_detail.html`. You can access the model `Quip`
with all its attributes under `{{ object }}` in the template. 

This is powerful. Instead of fussing about building a function that
fetches the correct object, finds a particular template, and then
fuses the two together, `DetailView` does all that for us and we only
need to tell it which model to use. 

The other detail here is that our `urlpatterns` looks for a parameter
`pk` to be an integer. This is the primary key for the database
lookup.

These defaults may not be ideal though. Perhaps we want our template
to have a different name, our model to be rendered in the template as
something other than `{{ object }}`, or a different url parameter to
be looked for than `pk`. We can replace these all easily:

```python
class QuipDetailView(DetailView):
    model = Quip
    context_object_name = "quip"  # replaces {{ object }} in the template
    pk_url_kwarg = "_id"  # replaces `pk` in the url lookup
    template_name = "new_quip_detail.html"  # replaces "quip_detail.html"
```

Keeping in mind these all get used in functions, we can overide those
functions as well. This is typically done for a query lookup.

Under the hood, `DetailView` is using
[`SingleObjectMixin`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin)
to call `def get_object(self, queryset=None)`. This will use either
the constant `self.queryset` or `def self.get_queryset()`. In both
cases, it expects a
[`queryset`](https://docs.djangoproject.com/en/3.1/ref/models/querysets/)
object from Django's ORM. 

If we provide the constant, we can use it to only look for specific attributes.

```python
class QuipDetailView(DetailView):
    model = Quip
    queryset = Quip.objects.values("content", "user.username")
```

Alternatively, we can replace the `def get_object` or `def
get_queryset` functions directly. This lets us be more dynamic.

```python
class QuipDetailView(DetailView):
    model = Quip

    def get_queryset(self):
        filter_by = self.kwargs['filter_by']  # url parameter
        return Quip.objects.filter(content_icontains=filter_by)
```

```python
# urls.py
from django.urls import path, include

from quips.views import *

urlpatterns = [
    path("c/<int:pk>/<str:filter_by>", QuipDetailView.as_view(), name="quip_detail"),
]
```

What about multiple objects instead of specific ones?

That would involve the `django.views.generic.ListView`. This works
identical to `DetailView` but will not look up an object by
`pk`. Instead it passes all the objects found as a list of
dictionaries to the template under `{{ objects }}`.

```python
from django.views.generic import ListView

class QuipDetailView(DetailView):
    model = Quip
```

We can tweak the specific queryset pased just like before, modifying
the `def get_queryset` function and `queryset` object variable. 

Your next thought is probably "How do I prevent authorized users from
viewing this?" which I get to later.

For now, let's trudge forward into editing classes. This will let us
post and get at data via forms in an expected way. 


## Editing CBVs -- `CreateView`, `UpdateView`, `DeleteView`

These fall under `django.views.generic.edit`:

  * [`django.views.generic.edit.CreateView`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView)

  * [`django.views.generic.edit.DeleteView`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView)

  * [`django.views.generic.edit.UpdateView`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView)


The names are straightforward to comprehend. They all subclass
`django.views.generic.edit.FormView`. Two words of note on that.

One, you don't actually need to pass in a `django.forms.Form`
object. You can opt to pass in a `model` variable and a list of
`fields` to include in the form. It will use defaults for all the
rendered fields (e.g. text boxes for `CharField`). 

Two, you can pass in a form object if you want. This is typically done
when rendering custom fields, using third party libraries like 
[`django-crispy-forms`](https://django-crispy-forms.readthedocs.io/en/latest/),
or you're converting pre-existing forms to CBVs.

If you pass both a `form_class` and `model` + `fields`, then Django
will raise an exception.

I find `FormView` never gets used in practice, you almost always end
up subclassing one of the three mentioned above. We'll look over those
as examples.

`CreateView` processes the `def get` and `def post` functions for
us. It excepts a URL with no parameters. If you send a GET request, it
will return a rendered template under
`<app-name>/<model-name>_form.html` and if you send a POST request, it
will create a new object or return an error if the form doesn't
validate.

`UpdateView` will expect a URL with a `pk` parameter. If given a GET
request, it will return the template
`<app-name>/<model-name>_form.html`. If you send a POST request, it
will look up the object by its primary key and update it with the
values passed. If it successfully updates, it will redirect to the
`success_url` variable. 


`DeleteView` will expect a URL with a `pk` parameter. If given a GET
request, it will return the template
`<app-name>/<model-name>_confirm_delete.html` where you usually ask
the user if they really want to delete. If given a POST request, it
will delete the object at `pk`. Upon successful deletion, it will
redirect to the `success_url` variable. 


To simplify understanding this, I've included a the view objects, the
url patterns, and skeleton html templates, passing in the defaults:

```python
# views.py
class QuipCreateView(CreateView):
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")
    context_object_name = "object"
    template_name = "quip_form.html"  


class QuipUpdateView(UpdateView):
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")
    pk_url_kwarg = "pk"
    template_name = "quip_form.html" 


class QuipDeleteView(DeleteView):
    model = Quip
    success_url = reverse_lazy("quip_list")
    pk_url_kwarg = "pk"
    template_name = "quip_confirm_delete.html"
```

```python
# urls.py
from django.urls import path, include

from quips.views import *

urlpatterns = [
    path("c/create_quip/", QuipCreateView.as_view(), name="quip_create"),
    path("c/update_quip/<int:pk>", QuipUpdateView.as_view(), name="quip_update"),
    path("c/delete_quip/<int:pk>", QuipDeleteView.as_view(), name="quip_delete"),
]
```

```html
<!-- quip_form.html -->

<div>
  <!-- action="<same-url-GET-if-not-mentioned>" -->
  <form method="POST">
    {% csrf_token %}
    {{ form.content }}
    <button type="submit">Submit New Quip</button>
  </form>
</div>
```

```html
<!-- quip_confirm_delete.html -->

<form method="POST">
  {% csrf_token %}
  <button type="submit">Delete Quip?</button>
</form>
```

This is good and all but there's a bit more we can do. Now that we
have the basic objects under our belt, let's look at overriding
certain functions and using mixins to save ourself repeat code
writes. 


## `LoginRequiredMixin` and `UserPassesTestMixin`

Django features many mixins, which we've used above. There are two
"utility" mixins that we can include to get extra functionality.

One is `LoginRequiredMixin`. It's usage is straight forward. It will
check that the user in question is logged in before returning the
view, other it will 403. This allows us to assume a `request.user`
object exists so we don't have to look for it with `if request.user:`
type statements. 

Two is `UserPassesTestMixin`. This will look for a function `def
test_func(self)` and check for a boolean return. If true, it will
return the view as normal. If false, it will raise a 403.

Let's go back to our `DeleteView` we wrote earlier. We don't want
users willy-nilly deleting object. We also don't want users who don't
own the particular object deleting them. We can use both
`LoginRequiredMixin` and `UserPassesTestMixin` to do this.

```python
# views.py
class QuipDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Quip
    success_url = reverse_lazy("quip_list")

    def test_func(self):
        """Check that the user owns this quip"""
        return self.get_object().user == self.request.user
```

You'll notice a couple things going on here.

One is that we have three
parent classes. Remember that we evaluate from left-to-right which
means that the object will attempt to evaluate a funtion under
`UserPassesTestMixin` first before going to `LoginRequiredMixin` and
then to `DeleteView`. This doesn't matter much here as there isn't any
overloaded functions but it will later.

Two is that we have a `def test_func` function defined. That's what
`UserPassesTestMixin` expects. Knowing that we can safely expect a
`self.user`, we can then check if the object requested is owned by
that user. I'll include the model code below to make this clear.

```python
# models.py
from django.db import models
from django.contrib.auth.models import User


class Quip(models.Model):
    # pk => primary key will be automatic
    content = models.CharField(max_length=360)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Perhaps a bit more obtuse is the `self.get_object()` call. This is not
stated directly in the docs. You need to glean it from one of its
parent mixins. In this case, that is
[`django.views.generic.detail.SingleObjectMixin`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin).

This approach can be expanded on down for all of the views. But that
would take a lot of time and violates DRY principles. Better is to
create your own mixins.


### Building your own Mixins to not repeat yourself

The following mixins are ones I commonly use. It's best to include
these in a separate `mixin.py` file for clean reading. Utility mixins
that aren't clearly under one app are best to be put under the
`accounts` app or equivalent. 

Here is the above code but factored out as a mixin.

```python
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class OwnedByUserMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        """Check that the user owns this quip"""
        return self.get_object().user == self.request.user


# views.py
class QuipDeleteView(OwnedByUserMixin, DeleteView):
    model = Quip
    success_url = reverse_lazy("quip_list")
```

Next is a mixin to assign any created object to the logged in user who
made a request. The `def form_valid` is called to validate a form. We
can "intercept" it and attach the user information before calling the
parent class' form validation.

```python
class AssignToUserMixin(LoginRequiredMixin):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# views.py
class QuipCreateView(AssignToUserMixin, CreateView):
    # quip_form.html
    model = Quip
    fields = ["content"]
    success_url = reverse_lazy("quip_list")
```

This mixin is effectively an interface. [As discussed before](\#), Python
will not check if `super().form_valid(form)` is valid. We know that
`def form_valid` is defined under
[`django.views.generic.edit.FormMixin`](https://docs.djangoproject.com/en/3.1/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin)
which is part of the `FormView` that `CreateView`, `UpdateView`, and
`DeleteView` all use.

Next is a mixin to add in the logged in user information as context
passed to the template. It's nice for user pages for getting the
logged in user's name. 

```python
class AddUserContextData(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
```

Lastly is a mixin to handle ajax requests. This will return a JSON
response instead of HTML when AJAX is used.

```python
class JsonResponseMixin(object):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({"url_redirect": "/"}, status=200)
        return response
```

An example jQuery that would use this is below.

```javascript
$('button').on('click', function(e) {
  e.preventDefault();
  console.log("clicked");
  $.post(
    "{% url 'quip_create' %}",
    $('form').serialize(),
    function(resp) {
      console.log("success!", resp);  // could also put in a loading element
      window.location.replace("/");
    }
  )
});
```

## User Authentication System

Django's built in user authentication system is one of the key
differences with Ruby-on-Rails.

It handles a lot of the basic cruft you'll have. It will hash
passwords, check for valid emails and usernames, and provide an
administrative interface.

It also includes a set of pre-built URLs to use. Things like login,
logout, password changes and resets. This is all boilerplate and
largely the same from project to project. Providing it upfront is
alleviating.

You could include this within the same app but as Django does not
provide user sign up or profile default views, I like to create a
separate `accounts` app.

To include these default urls, simply include the following.

```python
# urls.py
from django.urls import path, include


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
```

This is not much code to write but it opens up a host of default
routes to use. Each then corresponds to a particular default CBV which
will look for a default template. If you use only the defaults, highly
recommended when starting a project, this can be 

  * `login/` => django.contrib.auth.views.LoginView
    * looks for `registration/login.html`
    * route name is `login`
  * `logout/` => django.contrib.auth.views.LogoutView
    * looks for `registration/logged_out.html`
    ` route name is `logout`
  * `password_change/` => `django.contrib.auth.views.PasswordChangeView`
    * passes `{{ form }}` for password change
    * looks for `registration/password_change_form.html`
    * route name is `passowrd_change`
  * `password_change/done/` => `django.contrib.auth.views.PasswordChangeDoneView`
    * looks for `registration/password_change_done.html`
  * `password_reset/ => `django.contrib.auth.views.PasswordResetView`
    * for "I forgot my email login" requests
    * uses `registration/password_reset_form.html` on GET request, passes `{{ form }}`
    * uses `registration/password_reset_email.html` as the email template
    * uses `registration/password_reset_subject.txt` as the subject line
  * `reset/<uidb64>/<token>/` => `django.contrib.auth.views.PasswordResetConfirmView`
    * passes a `{{ form }}` for password change
    * uses `regisration/password_reset_confirm.html`
  * `reset/done/` => `django.contrib.auth.views.PasswordResetCompleteView`
    * uses `registration/password_reset_done.html`


Alternatively, you could write the following and overwrite/extend as
deemed necesary:

```python
# urls.py
from django.urls import path, include
from django.contrib.auth.views import (
  LoginView,
  LogoutView,
  PasswordChangeDoneView,
  PasswordResetView,
  PasswordResetConfirmView,
  PasswordResetCompleteView
)
  


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
```

Django includes default templates for all of these. I've included a
few very simple ones below you can use to start.

```html
<!-- registration/login.html -->
<h1>Login Page</h1>
<div>
  <a href="{% url 'password_reset' %}">Reset password via email</a>
</div>
<div>
  <form action="{% url 'login' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
  </form>
</div>


<!-- registration/logged_out.html -->
<h1>You have succesfully Logged Out</h1>


<!-- registration/password_change_form.html -->
<h1>Change Password you already know</h1>
<form method="POST"> <!-- will send to the same URL -->
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Change Password">
</form>


<!-- registration/password_change_done.html -->
<h1>Password Reset Complete</h1>


<!-- registration/password_reset_form.html -->
<h1>Forgot your password?</h1>
<form method="POST"> <!-- will send to the same URL -->
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Email me next steps">
</form>


<!-- regisration/password_reset_confirm.html -->
<h1>Change password you don't know</h1>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Change Password">
</form>


<!-- registration/password_reset_done.html -->
<h1>You're password has been reset</h1>
```


## Wrap-Up

...



# Cheat sheet to write

  * All seven objects
    * default values
    * functions w/what they do, split by which ancestor they get that from
