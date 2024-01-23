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
from ..views import clientes_sinc, controle_fundos_xp , pcos_em_lote , editar_fundos_xp , fundos_xp_atualizados , delete_fundo


urlpatterns = [
    path("sincronizar_clientes", clientes_sinc , name="sincronizar_clientes") ,
    path("fundos_xp", controle_fundos_xp, name="cadastro_fundos_xp"),
    path("pcos_em_lote", pcos_em_lote, name="lote_pcos"),
    path("editar_fundos_xp", editar_fundos_xp, name="editar_fundos_xp"),
    path("atualizar_cadastros" ,  fundos_xp_atualizados , name="atualizar_cadastro_fundos_xp") , 
    path("remover_fundo" , delete_fundo , name='excluir_fundos')


 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


