Changes from last project

  * add accounts as separate app
  * add in basic homepage that uses log in only
  * separate it with git more early on


Set up a basic twitter site
  * you can post and read other posts -- but only if logged in
  otherwise it redirects to a homepage 

Outline

  * explanation of "batteries-included" web frameworks and why they're
    powerful -- what the catch is 

    * force discipline on you while allowing you to move quickly

  * Django includes user management -- which is slightly unusual as most force you into their own
  *




```python
from django.contrib.auth.models import User
# will auto-committ to the database
user = User.objects.create_user(
    username='john',
    email='jlennon@beatles.com',
    password='glass onion')
```
