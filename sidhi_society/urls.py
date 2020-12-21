"""sidhi_society URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from accounts import views as acc_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from django.conf import settings
from employee.views import client_report
from django.conf.urls.static import static
from accounts.decorators import *

#  auth_views.LoginView.as_view(template_name='accounts/log.html' , extra_context={'title':"Login", 'pretext':'Already have ', 'url':'register' }) ,name = 'login')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bank/', include('employee.urls')),
    url(r'^$', client_report),
    url('login/', unauthenticated_user(auth_views.LoginView.as_view(template_name='accounts/log.html' , extra_context={'title':"Login", 'pretext':'Already have ', 'url':'register' })), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

]
   

