from django.shortcuts import render, redirect
from django.views.generic import View
from  .forms import SubsriptionForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
#from .import auth_forms



def subscription(request):
    if request.method == "POST":
        form = SubsriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
        return redirect("/login")
    else:
        form = SubsriptionForm()
    return render(request, "subscribe/subscribe.html", {"form":form})


def login(request):
    pass
    