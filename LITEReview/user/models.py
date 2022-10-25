from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image, ImageOps



class UserProfile(models.Model):#
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super().save()

        img = ImageOps.fit(
            Image.open(self.image.path),
            (300, 300),
            method=3,
            centering=(0.5, 0.5)
        )

        img.save(self.image.path)



class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Meta:
    # ensures we don't get multiple UserFollows instances
    # for unique user-user_followed pairs
    unique_together = ('user', 'followed_user', )

