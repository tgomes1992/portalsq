from django.shortcuts import render
from django.http import request , HttpRequest , HttpResponse
from .eventos_diarios import get_all_events_api , get_all_ifs
# from .CalculoDiaUtil import CalculoDiaUtil
from datetime import datetime
import csv


def homeEventos(request):
    hoje = datetime.today()
    ativos = get_all_ifs()

    if request.method == "POST":
        hoje = datetime.strptime(request.POST['data'], "%Y-%m-%d")

    dados  = {
        "dia":  hoje.strftime("%d/%m/%Y") ,
        "eventos" : get_all_events_api(hoje) ,
        # "diautil" : CalculoDiaUtil(hoje).calculardiautil() ,
        "ativos":   ativos
    }
    return render(request , "eventos/home.html" , dados)



def ativosCadastrados(request):
    hoje = datetime.today()
    ativos = get_all_ifs()
    dados = {
        "ativos":  ativos
    }
    return render(request , "eventos/ativos_cadastrados.html" , dados)



def download_ativos(request):
    ativos = get_all_ifs()
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="ativos.csv"'},
      )
    writer =  csv.writer(response , delimiter=";" )

    writer.writerow(["ativos"])
    for ativo in ativos:
       print (ativo)
       writer.writerow([ativo])

    return response





def eventosXp(request):
    hoje = datetime.today()
    dados = {
        "hoje" : datetime.today().strftime("%d/%m/%Y") , 
        # "diautil":  CalculoDiaUtil(hoje).calculardiautil()
    }
    return render(request , "eventos/EventosXP.html" , dados)



# Create your views here.
