from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, RegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from follow_auth.forms import FollowForm
from follow_auth.models import UserFollows
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account has been created for " + user)
        return redirect("/login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {"u_form": u_form, "p_form": p_form, "title": "Profile"}

    return render(request, "registration/profile.html", context)


@login_required
def follows_page(request):

    if request.method == "POST":
        form = FollowForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST["followed_user"])
                if request.user == followed_user:
                    messages.error(request, "You can't follow yourself!")
                else:
                    try:
                        UserFollows.objects.create(
                            user=request.user, followed_user=followed_user
                        )
                        messages.success(
                            request, f"You are now following {followed_user} !"
                        )

                    except IntegrityError:
                        messages.error(
                            request, f"You are already following {followed_user} !"
                        )

            except User.DoesNotExist:
                messages.error(
                    request, f'The user {form.data["followed_user"]} does not exist.'
                )

    else:
        form = FollowForm()

    user_follows = UserFollows.objects.filter(user=request.user).order_by(
        "followed_user"
    )
    followed_by = UserFollows.objects.filter(followed_user=request.user).order_by(
        "user"
    )

    context = {
        "form": form,
        "user_follows": user_follows,
        "followed_by": followed_by,
        "title": "Follows",
    }

    return render(request, "follow_auth/follow_page.html", context)


class UnfollowUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserFollows
    success_url = "/follow_page"
    context_object_name = "unfollow"

    def test_func(self):
        unfollow = self.get_object()
        if self.request.user == unfollow.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(
            self.request,
            f"You have stopped following {self.get_object().followed_user}.",
        )
        return super(UnfollowUser, self).delete(request, *args, **kwargs)
