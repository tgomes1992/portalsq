from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
import pandas as pd 
from ..controllers.FloatDiario import ArquivoFloatDiario
from io import BytesIO

# Create your views here.





def home_float(request):
    if request.method == 'POST':
        importador = ArquivoFloatDiario()
        importador.AtualizacaoFloatDiario(request.FILES['arquivo'])        
    return render(request, "sqdados/float.html")


def get_relatorio_float_mensal(request):
    df = ArquivoFloatDiario().gerar_relatorio_float_mensal()
    filename = f"float_mensal.xlsx"
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            df.to_excel(writer, sheet_name="float_mensal", index=False)
            return res
    

def get_relatorio_float_geral(request):
    df = ArquivoFloatDiario().gerar_relatorio_float_geral()
    filename = f"float_geral.xlsx"
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            df.to_excel(writer, sheet_name="float_geral", index=False)
            return res
