from django.shortcuts import render , redirect
from django.http import request , HttpRequest , HttpResponse
from ..eventos_diarios import get_all_events_api , get_all_ifs ,  engine ,  text , get_all_events_ativo
# from .CalculoDiaUtil import CalculoDiaUtil
from datetime import datetime
import csv
from ..buscar_emissores_o2 import get_emissor
from intactus.osapi import o2Api
from datetime import datetime , timedelta
from io import BytesIO
import pandas as pd
from ..models import FundoXP , EventosDiarios
from .ControleEventos import *
from django.db.models.functions import Cast
from django.db.models.functions import ExtractDay , ExtractHour , ExtractMinute , ExtractMonth , ExtractQuarter , ExtractYear ,  Concat
from django.db import models
from django.db.models import DateTimeField , IntegerField
from django.db.models import CharField, Value as V

def homeEventos(request):
    hoje = datetime.today()
  

    if request.method == "POST":
        hoje = datetime.strptime(request.POST['data'], "%Y-%m-%d")


    eventos = EventosDiarios.objects.annotate(month = ExtractMonth('data_liquidacao') ,
                                               year=ExtractYear("data_liquidacao"))\
                                    .values("month" , "year" , "ativo" , "emissor" , "data_liquidacao")\
                                    .filter(month = hoje.month , year=hoje.year)


    dados  = {
        "dia":  hoje.strftime("%d/%m/%Y") ,
        "eventos" : eventos  ,

    }
    return render(request , "eventos/home.html" , dados)



def baixar_eventos_excel(request):

    hoje = datetime.today()


    eventos = EventosDiarios.objects.annotate(month = ExtractMonth('data_liquidacao') ,
                                               year=ExtractYear("data_liquidacao") ,
                                               day = ExtractDay("data_liquidacao") )\
                                    .values("day" , "month" , "year" , "ativo" , "emissor" )\
                                    .filter(month = hoje.month , year=hoje.year)

 



    filename = f"eventos_diarios.xlsx"
    dataframes = pd.DataFrame.from_dict(eventos)
    dataframes['data_liquidacao'] = dataframes['day'].apply(str) + "/" + dataframes['month'].apply(str) + "/" + dataframes['year'].apply(str)


    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            dataframes[['ativo' , 'emissor' ,  'data_liquidacao']].to_excel(writer, sheet_name="eventos_diarios", index=False)
            return res




def excluir_ativo(request):

    ativo  =  request.GET['ativo']

    con = engine.connect()
    con.execute(text(f"delete from pmts where Título='{ativo}' "))
    con.commit()
    return redirect('ativoscomeventos')



def detalhe_ativos(request):
    ativo = request.GET['ativo']
    dados_ativo = EventosDiarios.objects.filter(ativo = ativo)
    dados = {
        "eventos": dados_ativo , 
        "ativo": ativo
    }

    return render(request , "eventos/cadastroAtivos.html" , dados)





def ativosCadastrados(request):
    hoje = datetime.today()
    eventos = [item.ativo for item in EventosDiarios.objects.all()]
    ativos = []
    for item in eventos:
        if item not in ativos:
            ativos.append(item)

    dados = {
        "ativos":  ativos
    }
    return render(request , "eventos/ativos_cadastrados.html" , dados)



def download_ativos(request):
    eventos = [item.ativo for item in EventosDiarios.objects.all()]
    ativos = []
    for item in eventos:
        if item not in ativos:
            ativos.append(item)
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
        "eventosXp": FundoXP.objects.all()
    }

    if request.method == 'POST':
        form = request.POST
        fundo = FundoXP(diaUtil = form['diautil'] ,fundo = form['fundo'] )
        fundo.save()

    return render(request , "eventos/EventosXP.html" , dados)

def remover_eventos_xp(request):
    id = request.GET['id']
    print (id)
    fundo = FundoXP.objects.filter(id=id)
    fundo.delete()


    return redirect('eventosxp')





# Create your views here.
