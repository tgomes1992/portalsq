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
from informes_legais.views import *



urlpatterns = [
    path("5401",  View_5401.as_view() , name="5401") ,
    path("efinanceira" , View_Efinanceira.as_view() , name="efinanceira") ,
    path("gerar_efin" , GeracaoEfin.as_view() , name="gerar_efin") ,



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
