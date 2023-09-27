
from django.shortcuts import render
from django.core.paginator import Paginator
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
    paginator = Paginator(arquivos , 10)
    page = request.GET.get("page")
    files_on_page = paginator.get_page(page)    
    return render(request , "xpapp/arquivosXpImportados.html" , {"arquivos": files_on_page})




def arquivos_estatisticas_view(request):
        id = request.GET.get('id')
        arquivo = ArquivosXp.objects.filter(id=id).first()
        movimentacoes = MovimentacoesXP.objects.filter(filename=arquivo.filename)

        return render(request , "xpapp/ArquivosEstatisticas.html" , {"movimentacoes":  movimentacoes} )
