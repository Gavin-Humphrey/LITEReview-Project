from django.shortcuts import render, redirect
#from django.views.generic import View
from  .forms import ProfileUpdate, SubsriptionForm, UserUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
#from .import auth_forms



def register(request):
    if request.method == "POST":
        form = SubsriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now log in.')
        return redirect("/login")
    else:
        form = SubsriptionForm()
    return render(request, "registration/register.html", {"form":form})



@login_required
def profile(request):
    if request.method == 'POST':
        user_update = UserUpdate(request.POST, instance=request.user)
        profile_update = ProfileUpdate(request.POST, request.FILES, instance=request.user.userprofile)#

        if user_update.is_valid() and profile_update.is_valid():
            user_update.save()
            profile_update.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        user_update = UserUpdate(instance=request.user)
        profile_update = ProfileUpdate(instance=request.user.userprofile)

    context = {
        'user_update': user_update,
        'profile_update': profile_update,
        'title': 'Profile'
    }

    return render(request, 'registration/profile.html', context)


