
from django.shortcuts import render , redirect
from ..controllers.Quantitativoo2 import *
from datetime import datetime
from django.http import HttpResponse
from io import BytesIO



def home_quantitativo(request):
    if request.method =='POST': 
        dados_request =  request.POST
        print (request.POST)
        if dados_request['tipoarquivo'] ==  "fundos":
            return  redirect('fundos_ativos' , data=datetime.strptime( request.POST['data'] ,"%d/%m/%Y").strftime("%Y-%m-%d"))
        else:
            return redirect('outros_ativos' , data=datetime.strptime( request.POST['data'] ,"%d/%m/%Y").strftime("%Y-%m-%d"))
            
    return render(request, "sqdados/quantitativo.html")



def list_fundos_ativos(request , data):
    print(data)
    data  = datetime.strptime(data,  "%Y-%m-%d" )
    fundos_ativos = CalculoQuantitativoO2(data).get_fundos_ativos()

    filename = f"fundos_ativos_{data.strftime('%Y-%m-%d')}.xlsx"
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            fundos_ativos.to_excel(writer, sheet_name="fundos_ativos", index=False)
            return res



def list_outros_ativos(request , data):
    data  = datetime.strptime(data,  "%Y-%m-%d" )
    fundos_ativos = CalculoQuantitativoO2(data).get_outros_ativos_ativos()
    filename = f"outros_ativos_{data.strftime('%Y-%m-%d')}.xlsx"
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            fundos_ativos.to_excel(writer, sheet_name="outros_ativos", index=False)
            return res