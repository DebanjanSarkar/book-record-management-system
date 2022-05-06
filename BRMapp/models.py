from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    #Changing the display name of the record objcets of this table in the django admin app
    def __str__(self):
        return self.title

class BRMuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20,null=False)
    #Changing the display name of the record objcets of this table in the django admin app
    def __str__(self):
        return self.nickname
    #Changing the display name of this table in the Django admin app
    class Meta:
        verbose_name_plural = "Book Record Management Users"
