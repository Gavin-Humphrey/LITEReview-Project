from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone


# feeds/models.py

class Ticket(models.Model):
    title = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, null=True, upload_to='reviews_img')

    def __str__(self):
        return f'Ticket-{self.title}'

class Review(models.Model):
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)  
      
    def __str__(self):
        return f'Review-{self.headline}'