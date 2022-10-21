from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image, ImageOps



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    




