
from django.shortcuts import render ,  redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from ..models import MovimentacoesXP , FundoXP ,  ArquivosXp
from ..xphelper import CadastroFundosXP




def fundos_xp_atualizados(request):
    controle = CadastroFundosXP()
    controle.atualizar_cadastros()
    controle.atualizar_dados_o2()

    return HttpResponse("done")





def controle_fundos_xp(request):
    fundos = FundoXP.objects.all()
    if request.method =='POST':
        dados_request = request.POST
        fundo = FundoXP(nome = dados_request['fundo_nome'] ,
                        cd_jcot=dados_request['cd_jcot'] ,
                        cnpj = dados_request['fundo_cnpj'] , 
                        filename = dados_request['filename'])                      

        fundo.save()
        fundos = FundoXP.objects.all()

    return render(request , "xpapp/controle_fundos.html" , {"fundos": fundos} )


def editar_fundos_xp(request):
     if request.method == "GET":
            cd_jcot = request.GET.get('id')
            fundo = FundoXP.objects.filter(cd_jcot=cd_jcot).first()
            return  render(request , "xpapp/editar_fundos.html" , {"fundo":  fundo})
     else:
            dados_request = request.POST
            fundo = FundoXP(nome = dados_request['fundo_nome'] ,
                        cd_jcot=dados_request['cd_jcot'] ,
                        cnpj = dados_request['fundo_cnpj'] , 
                        filename = dados_request['filename'])                      

            fundo.save()
            return redirect('cadastro_fundos_xp')


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
