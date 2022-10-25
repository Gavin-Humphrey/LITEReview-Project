from django.contrib import admin
from .models import UserProfile 
from feeds.models import Ticket, Review

admin.site.register(UserProfile) 
admin.site.register(Ticket)
admin.site.register(Review)


