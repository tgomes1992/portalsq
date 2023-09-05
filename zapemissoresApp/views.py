from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
from datetime import datetime
from .ControllerZAP import ControllerZAP



# Create your views here.



def main_emissores(request):
    if request.method == 'POST':
        data = datetime.strptime(request.POST['datasaldo'] , "%Y-%m-%d")
        df = ControllerZAP().get_saldos(data)
        print (df)
    else:
       df = ControllerZAP().get_saldos(datetime.today())


    dados = {
        "emissores" : df.sort_values(by=['ValorSaldoTotal'], ascending=False).to_dict("records")
    }

    return render(request,"zapemissoresapp/base.html" , dados)
