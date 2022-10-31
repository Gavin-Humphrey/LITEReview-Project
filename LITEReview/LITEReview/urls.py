"""LITEReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as reg_views
from feeds import views as views
from django.conf import settings
from django.conf.urls.static import static
from users import views as f_views
from feeds.views import edit_ticket, edit_review



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', reg_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', reg_views.profile, name='profile'),
    path('follow_page/', f_views.follows_page, name='follows_page'),
    path('confirm_unfollow/<int:pk>/', f_views.UnfollowUser.as_view(), name='confirm-unfollow'),
    path('', include("django.contrib.auth.urls")),
    path('feeds-home/', views.feeds, name='feeds-home'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('create-review/<int:ticket_id>/', views.create_review, name='create_review'),
    path('create-ticket/', views.create_ticket_and_review, name='create_ticket_and_review'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

