from django.shortcuts import render
from django.http import HttpResponse
from .app_control import Ativoso2Sinc
from .app_control.batimento_diario_ import BatimentoDiario
from io import BytesIO
import pandas as pd
# Create your views here.



def home_conciliacao_app(request):
    return render(request, 'conciliacao/conciliacao.html'  )

def validar_conciliacao_diaria(request):
    ativos_o2 = Ativoso2Sinc()
    ativos = ativos_o2.get_cds_o2()
    dados = {
        "ativos": ativos
    }

    if request.method == 'POST':

        ativos_o2 = Ativoso2Sinc().get_ativos_unique(request.POST['ativo'])
        batimento = BatimentoDiario()
        df = batimento.consolidar_posicao(ativos_o2 , request.POST['data'])

        filename = f"batimentosdiarios.xlsx"
        dataframes = df
        with BytesIO() as b:
            res = HttpResponse(
                b.getvalue(),  # Gives the Byte string of the Byte Buffer object
                content_type="application/xlsx",
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
            with pd.ExcelWriter(res) as writer:
                dataframes.to_excel(writer, sheet_name="batimentos_diarios", index=False)
                return res

    return render(request, 'conciliacao/validar_conciliacao.html' , dados )



def sinc_ativos_o2(request):
    Ativoso2Sinc().get_ativos_extracao()
    return render(request, 'conciliacao/ativos.html'  )

def listar_ativos_o2(request):
    ativos_o2 = Ativoso2Sinc()
    ativos = ativos_o2.get_ativos_o2_list()
    dados = {
        "ativos": ativos
    }
    return render(request, 'conciliacao/ativos_o2.html' ,  dados )



def get_ativos_o2_relatorio(request):

    df = Ativoso2Sinc().get_ativos_relatorio()
    output = BytesIO()

    chunk_size = 10000

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for i in range(0, len(df), chunk_size):
            df_chunk = df.iloc[i:i + chunk_size]
            df_chunk.to_excel(writer, sheet_name='ativos_o2', startrow=i, index=False, header=(i == 0))
        writer.save()

    # Set the buffer's cursor position to the beginning
    output.seek(0)

    # Create a Django response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = f'attachment; filename=relatorio_ativos.xlsx'
    response.write(output.getvalue())

    return response