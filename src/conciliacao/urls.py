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
from conciliacao.views import *



urlpatterns = [
    path("",  home_conciliacao_app , name="conciliacao_app") ,
    path("sinc_ativos",  sinc_ativos_o2 , name="sinc_ativos_o2") ,
    path("lista_ativos",  listar_ativos_o2 , name="lista_ativos") ,
    path("validar_conciliacao_diaria",  validar_conciliacao_diaria , name="validar_conciliacao_diaria") ,
    path("get_relatorio_excel", get_ativos_o2_relatorio, name="get_relatorios_excel")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
