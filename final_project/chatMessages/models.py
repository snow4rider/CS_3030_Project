from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=150)
    recipient = models.CharField(max_length=150)