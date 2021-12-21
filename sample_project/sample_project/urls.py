"""sample_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from sample_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('sample_app/', include('sample_app.urls')), #including all the urls in sample_app/urls.py
    path('logout/', views.user_logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#The last bit above is to place the media folders on the url so
#their content can be served in the browser (e.g. in the Admin page) -
#this is not taught in the Udemy course but comes from here:
#https://docs.djangoproject.com/es/3.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
