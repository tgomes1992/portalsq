from ..xphelper import ControleImportacaoArquivoDiario , InvestidoresSinc ,  MovimentosSinc
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import pandas as pd
from ..models import FundoXP
from JCOTSERVICE import Mancotistav2Service , ManClienteService
from datetime import datetime
from ..forms import ImportacaoArquivosDiarios , ProcessarMovimentacoes , PCOS_LOTE



def importacao_arquivo_diario(request):
    form = ImportacaoArquivosDiarios()

    if request.method == "POST":
        ControleImportacaoArquivoDiario(request.FILES['arquivo'] , str(request.FILES['arquivo'])).get_file_data()
    
    return render(request,"xpapp/importacao_xp.html" , {'form':form})


def pcos_em_lote(request):
    form = PCOS_LOTE()
    cotista_service =  Mancotistav2Service("roboescritura","Senh@123")
    cliente_service = ManClienteService("roboescritura","Senh@123")
    if request.method == "POST":
        df = pd.read_excel(request.FILES['arquivo'])
        for investidor in df.to_dict("records"):
            cliente_service.request_cadastrar_clientes_pco_xp(investidor['codigo'] ,  investidor['nome'])
            cotista_service.request_habilitar_pco_xp_v2(investidor['codigo'])


    return render(request,"xpapp/importacao_lote_pco.html" , {'form': form})




def clientes_sinc(request):
    sinc_investidores = InvestidoresSinc()
    sinc_investidores.sincronizar_investidores_xp()
    return HttpResponse("<h1>Sincronização Concluída</h1>")



def sincronizar_lancamentos(request):
    form = ProcessarMovimentacoes()
    fundos = [{"cnpj": fundo.cnpj  , "nome":fundo.nome } for fundo in FundoXP.objects.all()]
    context = {
           "fundos": fundos , 
           'form': form
        }
    if request.method == "POST":
        fundo_INPUT = request.POST['fundo']
        fundo = FundoXP.objects.filter(nome=fundo_INPUT).first().cnpj
        data_movimentos = datetime.strptime( request.POST['dataMovimentacoes'] , "%Y-%m-%d").strftime("%Y-%m-%d")
        print (request.POST)
        movimentos_sinc = MovimentosSinc()  
        filename = f"lancamentos.xlsx"
        dataframes = movimentos_sinc.sincronizar_movimentos(fundo , data_movimentos)
        with BytesIO() as b:
            res = HttpResponse(
                b.getvalue(),  # Gives the Byte string of the Byte Buffer object
                content_type="application/xlsx",
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
            with pd.ExcelWriter(res) as writer:
                pass
                dataframes['lancamentos'].to_excel(writer, sheet_name="lancamentos_sincronizados", index=False)
                dataframes['log'].to_excel(writer, sheet_name="LOG", index=False)

                return res

    else:
        return render(request, "xpapp/lancamento_movimentacoes.html" ,  context)


