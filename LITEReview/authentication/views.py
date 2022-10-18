from django.shortcuts import render, redirect
from django.views.generic import View
from  .forms import SubsriptionForm
from django.conf import settings
#from .import auth_forms



def subscription(request):
    if request.method == "POST":
        form = SubsriptionForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("/login")
    else:
        form = SubsriptionForm()
    return render(request, "authentication/subscription.html", {"form":form})