from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notebook(models.Model):
    name = models.CharField(max_length=256, null=True)
    data = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

 

