from django.shortcuts import render , redirect
from django.http import HttpResponse
from ..models import FundoXP
from datetime import datetime
from JCOTSERVICE import ConsultaMovimentoPeriodoV2Service



def relatorios_diarios_xp(request):
    return render(request,"xpapp/relatorios_diarios_xp.html" )




def relatorio_movimentacao(request):
    if request.method == 'POST':
        service_movimentos = ConsultaMovimentoPeriodoV2Service("roboescritura" , "Senh@123")
        fundos = FundoXP.objects.all() 
        data = datetime.strptime(request.POST['data'] , "%d/%m/%Y")
        JOBS = [item.gerar_movimentos(data) for item in fundos]
        extracao = []
        for item in JOBS:
            for linha in item:
                extracao.append(linha)
        df = service_movimentos.montar_retorno_xp(extracao)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="OT_ORDENS_ENVIO_RETORNO_{data.strftime("%Y_%m_%d")}.csv"'
        df["Conta Corrente"] = ""
        df['Ponto Venda'] = ""


        # Write the DataFrame to the response
        formato = ["Numero Operacao","Investidor" , "Conta Corrente" , "Papel Cota","Ponto Venda","Tipo Operacao","Data Operacao","Data Conversao","Data Liquidacao",
    "Data do Fundo na Movimentacao","Valor","Status","Status Conversao",   "CNPJ do fundo" ]
            
        df[formato].to_csv(response, index=False , sep=";" )
        return response
