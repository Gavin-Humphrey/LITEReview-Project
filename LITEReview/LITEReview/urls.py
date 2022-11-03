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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as reg_views
from feeds import views as d_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as f_views
from feeds.views import TicketDeleteView, ReviewDeleteView






urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', reg_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', reg_views.profile, name='profile'),

    path('feeds-home/', d_views.feeds, name='feeds-home'),
    path('my_posts/', d_views.user_posts, name='my-posts'),
    path('user_posts/<int:pk>/', d_views.user_posts, name='user-posts'),

    path('', include("django.contrib.auth.urls")),
    path('follow_page/', f_views.follows_page, name='follows_page'),
    path('confirm_unfollow/<int:pk>/', f_views.UnfollowUser.as_view(), name='confirm-unfollow'),
   
    path('create-ticket/', d_views.create_ticket, name='create-ticket'),
    path('ticket/<int:pk>/detail/', d_views.ticket_detail, name='ticket-detail'),
    path('ticket/<int:pk>/update/', d_views.ticket_update, name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),

    path('create-review/', d_views.create_review, name='create-review'),
    path('review/response/<int:pk>', d_views.review_response, name='response-review'),
    path('review/<int:pk>/detail', d_views.review_detail, name='review-detail'),
    path('review/<int:pk>/update/', d_views.review_update, name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

