from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Chat")
    details = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
