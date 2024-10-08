from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=300)
    members = models.ManyToManyField(User, related_name="teams")
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.name