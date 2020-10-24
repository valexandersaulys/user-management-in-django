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
    * e
    
  


________________________

Snippets

```python
from django.contrib.auth.models import User
# will auto-committ to the database
user = User.objects.create_user(
    username='john',
    email='jlennon@beatles.com',
    password='glass onion')
```
