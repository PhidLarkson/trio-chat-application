from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

    
class Room(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.uuid4, max_length=16)
    name = models.CharField(blank=True, max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}|{self.id}"
    
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}"
