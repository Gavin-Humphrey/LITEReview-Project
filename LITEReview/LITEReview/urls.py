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
#from feeds.views import create_review
from users import views as reg_views
from feeds import views as feeds_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as f_views
#from feeds.views import create_ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', reg_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', reg_views.profile, name='profile'),
    path('follow_page/<int:pk>/', f_views.follows_page, name='follow-page'),
    path('', include("django.contrib.auth.urls")),
    path('feeds-home/', feeds_views.feeds, name='feeds_home'),
    path('create-ticket/', feeds_views.create_ticket, name='create_ticket'),
    path('create-review/', feeds_views.create_review, name='create_review'),
    path('create-review/', feeds_views.create_ticket_and_review, name='create_ticket_and_review'),
    #path('user-follow/', f_views.follows_search, name='user_follow'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

