from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Todo(models.Model):
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="pending")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description    
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        super().save(*args, **kwargs)
# Create your models here.
