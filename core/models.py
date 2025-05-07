from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField()

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.app.name}'
