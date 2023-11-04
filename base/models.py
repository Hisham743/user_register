from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(null=True, max_length=150)
    prof_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = models.CharField(null=True, max_length=150)
    bio = models.TextField(null=True)
