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
from xpapp.views import *



urlpatterns = [
    path("",  home_page_xp_app , name="home_xp_app") ,
    path("importacao_arquivo_diario", importacao_arquivo_diario, name="importar_arquivo_diario") ,
    path("movimentacoes_xp", movimentacoes_xp, name="movimentacoes_xp") ,
    path("relatorios_diarios_xp", relatorios_diarios_xp, name="relatorios_diarios") ,
    path("sincronizar_clientes", clientes_sinc , name="sincronizar_clientes") ,
    path("fundos_xp", controle_fundos_xp, name="cadastro_fundos_xp"),
    path("processar_movimentacoes", sincronizar_lancamentos, name="processar_movimentacoes"),
    path("arquivos_importados", arquivos_importados_view, name="arquivos_importados_xp"),
    path("dados_arquivos", arquivos_estatisticas_view, name="dados_arquivos"),
    path("relatorio_movimentacao" , relatorio_movimentacao , name="relatorio_movimentacao_xp") , 
    path("editar_fundos_xp" , editar_fundos_xp , name="editar_fundos_xp") , 
    path("get_arquivo_retorno" , DownloadZipView.as_view() , name="arquivo_retorno") ,
    path("pcos_em_lote" , pcos_em_lote , name="lote_pcos") 



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


