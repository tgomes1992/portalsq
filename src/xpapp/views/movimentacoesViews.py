from django.shortcuts import render
from django.http import HttpResponse
from ..models import MovimentacoesXP , FundoXP



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



def processar_movimentacoes(request):

    print ("a")

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
           "fundos": fundos
        }
        


    return render(request, "xpapp/lancamento_movimentacoes.html" , context)
