from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    phone_number = models.CharField(max_length=13)
