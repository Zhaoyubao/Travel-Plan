from __future__ import unicode_literals
from django.db import models
from ..login_register.models import User

class Travel(models.Model):
    destination = models.CharField(max_length=55)
    plan = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    users = models.ManyToManyField(User, related_name='travels')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
