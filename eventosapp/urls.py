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
from listfundos.views import  *
from eventosapp.views import *



urlpatterns = [
    path("",  homeEventos , name="eventosdiarios") ,
    path("eventosAtivosCadastrados" , ativosCadastrados , name="ativoscomeventos") ,
    path ("eventosXp" ,  eventosXp , name="eventosxp") , 
    path("eventos_diarios" , baixar_eventos_excel ,  name="eventos_diarios") ,  
    path("eventosxpexcluir" ,  remover_eventos_xp ,  name="excluir_eventos") , 
    path ("downloadativos" , download_ativos ,  name="downloadativoseventos") , 
    path ("excluir_ativo_pmt", excluir_ativo ,  name="excluir_ativo" ) , 
    path ("consulta_ativo" , detalhe_ativos , name="consulta_ativo")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
