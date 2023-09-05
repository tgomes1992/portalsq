"""portalescrituracao URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
from emissoresapp.views import *



urlpatterns = [
    path("",  home_emissores_app , name="home_emissores_app") ,
    path("o2sinc",  o2sinc , name="o2sinc") ,
    path("emails",  cadastro_emails , name="emailemissores") ,

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
