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
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from ..views import  relatorios_diarios_xp , \
    arquivos_importados_view , arquivos_estatisticas_view , \
    relatorio_movimentacao ,liberar_lancamento , DownloadZipView , ProcessJobsView


urlpatterns = [
    path("relatorios_diarios_xp", relatorios_diarios_xp, name="relatorios_diarios") ,
    path("arquivos_importados", arquivos_importados_view, name="arquivos_importados_xp"),
    path("dados_arquivos", arquivos_estatisticas_view, name="dados_arquivos"),
    path("relatorio_movimentacao" , relatorio_movimentacao , name="relatorio_movimentacao_xp") ,
    path("get_arquivo_retorno" , DownloadZipView.as_view() , name="arquivo_retorno") ,
    path("liberar_lancamento/<int:id>" , liberar_lancamento , name="liberar_lancamento") ,
    path("processjobs" ,  ProcessJobsView.as_view() , name="processar_jobs" )

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


