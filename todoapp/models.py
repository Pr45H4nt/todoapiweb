from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    Title = models.CharField(max_length=1000)
    Description = models.TextField(blank=True)
    Completed = models.BooleanField(default=False)
    Date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.Title)


        