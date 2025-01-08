from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=80)
    fname = models.CharField(max_length=89)
    lname = models.CharField(max_length=88)
    email = models.EmailField(max_length=90)
    pass1 = models.CharField(max_length=90)
    pass2 = models.CharField(max_length=90)