from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name='owner')
    member = models.ManyToManyField(User, related_name='member')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return "player uid:" + str(self.player_uid)
