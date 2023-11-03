from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
from datetime import datetime
from .ControllerZAP import ControllerZAP
from io import BytesIO
import pandas as pd


# Create your views here.



def main_emissores(request):
    if request.method == 'POST':
        data = datetime.strptime(request.POST['datasaldo'] , "%Y-%m-%d")
        df = ControllerZAP().get_saldos(data)
        excel_download = BytesIO()
        writer = pd.ExcelWriter(excel_download, engine='openpyxl')
        df.to_excel(writer, sheet_name='file', index=False)
        writer.save()

        response = HttpResponse(
            excel_download.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="saldo_emissores_zap.xlsx"'

        return response


    else:
       df = ControllerZAP().get_saldos(datetime.today())


    dados = {
        "emissores" : df.sort_values(by=['ValorSaldoTotal'], ascending=False).to_dict("records")
    }

    return render(request,"zapemissoresapp/base.html" , dados)
