# README

Major points

  * Assusmptions at start about knowing Django with recs if you don't
  
  * Motivation: Why Use Class Based Views in Django?
    * allows you to move quickly, less cruft
    * enforces standards
    
  * The Catch: little immeadiate feedback & having to learn defaults
  
  * Separating concerns -- accounts app will be separate
  
  * Basic Class Based Views for Quips
  
  * Leveraging Class Based Views for Users

  * Building user sign up with CBVs
  
  * Leveraging Mixins to Quickly protect your app behind accounts
  
  * Extending User account details with OneToOne relationships

    * does not autocreate! (very frustrating)
    * you can overwrite the save function... bad idea
    * better to create a signal -- `signals.py` if you have a lot
    
  


________________________

Snippets

```python
from django.contrib.auth.models import User

# will auto-committ to the database
# will work for any django.db.models.Model object
user = User.objects.create_user(
    username='john',
    email='jlennon@beatles.com',
    password='glass onion')
```


Cheat Sheet -- does this make more sense as a three column thing?

  * for each CBV -- mention multiple ways to do things
    * the full path name
    * what's it for
    * what do you have to minimally provide
    * default template name + context
    * expectations from url (i.e. `<int:pk>`)

  * common keywords + functions in CBVs

  * the two available mixins

  * my added mixins



Cheat Sheet List

  * `django.views.generic.ListView`
    * For displaying a list of objects
    * Minimal Variables
      * `model`: the model object it lists
      * _or_ `get_queryset(self)`: returns the queryset of objects to list`
    * Extras
      * `paginate_by` 
    * Default Template: `<app-name>/<model-name>_list.html`
      * `objects`
    * URL expectations? No

  * `django.views.generic.DetailView`
    * Displaying the details of one object
    * Minimal Variables
      * `model`: the model object it lists
      * _or_ `get_queryset(self)`: returns object as type queryset
    * Extras -- none
    * default Template: `<app-name>/<model-name>_detail.html`
      * found object as `object`
    * URL expectations? `<int:pk>`

  * `django.views.generic.TemplateView`
    * for displaying a page
    * Minimal Variables
      * `template_name`: relative to `templates/` 
    * Extras
      * may want to overwrite `get_context_data(self, **kwargs)`
    * URL Expectations? No
     
  * `django.views.generic.edit.CreateView`
    * for displaying a form to edit a page
    * Minimal Variables
      * `model`: name of model to use
      * `fields`: list of string fields from model to include
      * `success_url`: `reverse_lazy("<name-of-view>")` after creation
    * Extras
      * `form_class`: can be specified in place of model and fields
    * Default template: `<app-name>/<model-name>_form.html`
      * `form`
    * URL expectations? No

  * `django.views.generic.edit.UpdateView`
    * for displaying an update view
    * Minimal Variables
      * `model`: name of model to use
      * `fields`: list of string fields from model to include
      * `success_url`: `reverse_lazy("<name-of-view>")` to rediect to
    * Extras
      * `form_class`: can be specified in place of model and fields
    * Default template: `<app-name>/<model-name>_form.html`
      * `form`
    * URL expectations: `<int:pk>` to update

  * `django.views.generic.edit.DeleteView`
    * for deleting a given object
    * Minimal Variables
      * `model`: name of model to use
      * `success_url`: `reverse_lazy("<name-of-view>")` after deletion
    * Default template: `<app-name>/<model-name>_confirm_delete.html`
      * `form`
    * URL expectations: `<int:pk>` to delete


Useful Keywords

  * `context_object_name`: rename `object[s]` in the template
  * `template_name`: change the template name to use
  * `get_queryset(self, **kwargs)`
  * `form_valid(self, form)`
  * `get_context_data(self, **kwargs)`


Useful Mixins

```python
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class OwnedByUserMixin(UserPassesTestMixin):
    def test_func(self):
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
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({"url_redirect": "/"}, status=200)
        return response
```
