from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    recipient = models.CharField(max_length=150)