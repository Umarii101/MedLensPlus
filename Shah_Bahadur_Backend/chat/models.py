from django.db import models

class Chat(models.Model):
    details = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)