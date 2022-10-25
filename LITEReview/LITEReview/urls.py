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
from user import views as reg_views
from feeds import views as feeds_views
from django.conf import settings
from django.conf.urls.static import static
#from feeds.views import create_ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', reg_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', reg_views.profile, name='profile'),
    path('', include("django.contrib.auth.urls")),
    path('feeds-home/', feeds_views.feeds, name='feeds-home'),
    path('create-ticket/', feeds_views.create_ticket, name='create_ticket'),
    path('create-review/', feeds_views.create_review, name='create_review'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

