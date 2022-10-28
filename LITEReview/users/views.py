from django.shortcuts import render, redirect
from  .forms import ProfileUpdateForm, RegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from follow_auth.forms import FollowForm
from follow_auth.models import UserFollows
from django.db import IntegrityError




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created for' + user)
        return redirect("/login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile'
    }

    return render(request, 'registration/profile.html', context)



@login_required
def follows_page(request):
    
    if request.method == 'POST':
            form = FollowForm(request.POST)

            if form.is_valid():
                try:
                    followed_user = User.objects.get(username=request.POST['followed_user'])
                    if request.user == followed_user:
                        messages.error(request, 'You can\'t follow yourself!')
                    else:
                        try:
                            UserFollows.objects.create(user=request.user, followed_user=followed_user)
                            messages.success(request, f'You are now following {followed_user}!')
                        except IntegrityError:
                            messages.error(request, f'You are already following {followed_user}!')

                except User.DoesNotExist:
                    messages.error(request, f'The user {form.data["followed_user"]} does not exist.')

            else:
                form = FollowForm()

                user_follows = UserFollows.objects.filter(user=request.user).order_by('followed_user')
                followed_by = UserFollows.objects.filter(followed_user=request.user).order_by('user')

                context = {
                    'form': form,
                    'user_follows': user_follows,
                    'followed_by': followed_by,
                    'title': 'Subscriptions',
                }

                return render(request, 'feeds/follow_page.html', context)

