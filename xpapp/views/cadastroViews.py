
from django.shortcuts import render
from django.http import HttpResponse
from ..models import MovimentacoesXP , FundoXP ,  ArquivosXp


def controle_fundos_xp(request):
    fundos = FundoXP.objects.all()
    if request.method =='POST':
        dados_request = request.POST
        fundo = FundoXP(nome = dados_request['fundo_nome'] ,
                        cd_jcot=dados_request['cd_jcot'] ,
                        cnpj = dados_request['fundo_cnpj'])
        fundo.save()
        fundos = FundoXP.objects.all()

    return render(request , "xpapp/controle_fundos.html" , {"fundos": fundos} )



def arquivos_importados_view(request):
    arquivos = ArquivosXp.objects.all()
    return render(request , "xpapp/arquivosXpImportados.html" , {"arquivos": arquivos})


