from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse , JsonResponse
from ..models import MovimentacoesXP , FundoXP
from ..forms import ProcessarMovimentacoes




def fundos_json(request):
    fundos = FundoXP.objects.all()
    fundos_json = {fundo.nome: "" for fundo in fundos}
    return JsonResponse(fundos_json , safe=False)






def movimentacoes_xp(request):
    movimentacoes  =  MovimentacoesXP.objects.all()

    for m in movimentacoes:
        print (m.cd_fundo)

    movimentos_a_sincronizar = [{"cd_investidor": movimento.cd_investidor ,
                                  "tipo_movimentacao": movimento.tipo_movimentacao  , 
                                  "cd_fundo": movimento.cd_fundo,   
                                  "valor": movimento.valor ,
                                   "filename": movimento.filename } for movimento in movimentacoes if not movimento.statusJcot]
    
    
    dados = {
        "movimentos": movimentos_a_sincronizar , 

    }
    return render(request,"xpapp/movimentacoes_xp.html" ,  dados)


def liberar_lancamento(request , id) :
    ajustado = int(id)
    movimento = MovimentacoesXP.objects.filter(id = ajustado).first()
    movimento.statusJcot = False
    movimento.save()
    return  JsonResponse({"message": "movimento reabilitado"})





def processar_movimentacoes(request):
    form = ProcessarMovimentacoes()


    if request.method =='POST':
        fundo = request.POST['fundo']
        print (request.POST)
        data_movimentacoes = request.post['dataMovimentacoes']
        movimentos = MovimentacoesXP.objects.filter(cd_fundo=fundo, statusJcot=False).values

        context = {
            "movimentos": movimentos , 

        }

    else:
        fundos = [{"cnpj": fundo.cnpj  , "nome":fundo.nome } for fundo in FundoXP.objects.all()]
        print (fundos)

        context = {
           "form": form
        }
        


    return render(request, "xpapp/lancamento_movimentacoes.html" , context)
