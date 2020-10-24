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


Cheat Sheet pieces

  * for each CBV -- mention multiple ways to do things
    * the full path name
    * what's it for
    * what do you have to minimally provide
    * default template name + context
    * expectations from url (i.e. `<int:pk>`)

  * useful keywords for CBVs

  * the two available mixins

  * my added mixins



Cheat Sheet List

  * django.views.generic.ListView
    * For displaying a list of objects
    * Minimal Variables
      * `model`: the model object it lists
      * _or_ `get_queryset(self)`: returns the queryset of objects to list`
    * Extras
      * `paginate_by` 
    * Looks in `<app-name>/<model-name>_list.html`
    * No URL expectations

  * django.views.generic.DetailView
  * django.views.generic.TemplateView
  * django.views.generic.edit.CreateView
  * django.views.generic.edit.UpdateView
  * django.views.generic.edit.DeleteView
