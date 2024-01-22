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

from sqdados.views import *



urlpatterns = [
    path("",  home_sq_dados , name="sqdados") ,
    path("float" , home_float , name="calculo_float") ,
    path("float_mensal" , get_relatorio_float_mensal , name="float_mensal") , 
    path("float_geral" , get_relatorio_float_geral , name="float_geral") , 
    path("quantitativo" , home_quantitativo , name="quantitativo") , 
    path('fundos_ativos/<str:data>' , list_fundos_ativos , name="fundos_ativos") , 
    path('outros_ativos/<str:data>' , list_outros_ativos , name="outros_ativos") , 
    path("volumes" , home_volumes , name='volumes') , 
    path("importacao_d_conciliacao" , importacao_arquivo_dconciliacao , name="importacao_d_dconciliacao") ,
    path("importar_arquivo_security_list" , importar_arquivo_securityList , name="arquivo_security_list") ,
    path("processar_volumes" , processar_volumes , name="processar_volumes") ,
    path("remunera" , home_remuneracao , name="remuneracao")  , 
    path("atualizar_codigos_ot" , atualizar_codigos_ot , name="get_cd_ot")  , 
    path("importar_arquivo_remunera" , importar_arquivo_remunera , name="importar_arquivo_remunera") ,
    path("remuneracoes_ativas" , remuneracoes_ativas , name="remuneracoes_ativas") ,
    path('cadastrar_receita_mensal', cadastrar_nova_remuneracao, name='cadastrar_receita_mensal'),
    path('editar_remuneracao/<int:id>', AtualizarReceita.as_view(), name='editar_remuneracao'),


    path('relatorios_remuneracao', relatorios_remuneracao, name='relatorios_remuneracao'),
   

    # path("eventosAtivosCadastrados" , ativosCadastrados , name="ativoscomeventos") ,

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
