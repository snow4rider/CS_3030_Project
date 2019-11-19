from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # username, first_name, last_name, date_joined and email already in AbstractUser
    description = models.CharField(max_length=500, unique=False, blank=True, null=False, default="")
    img_profile = models.CharField(max_length=100, unique=False, blank=True, null=False, default="")