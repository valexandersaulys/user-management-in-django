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

  * for each CBV
    * the full path name
    * what do you have to minimally provide
    * default template name + context

  * useful keywords for CBVs

  * the two available mixins

  * my added mixins
