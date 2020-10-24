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
