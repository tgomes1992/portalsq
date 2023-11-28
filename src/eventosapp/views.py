from django.shortcuts import render , redirect
from django.http import request , HttpRequest , HttpResponse
from .eventos_diarios import get_all_events_api , get_all_ifs ,  engine ,  text , get_all_events_ativo
# from .CalculoDiaUtil import CalculoDiaUtil
from datetime import datetime
import csv
from .buscar_emissores_o2 import get_emissor
from intactus.osapi import o2Api
from datetime import datetime
from io import BytesIO
import pandas as pd
from .models import FundoXP



def homeEventos(request):
    hoje = datetime.today()

    api =  o2Api("thiago.conceicao","DBCE0923-9CE3-4597-9E9A-9EAE7479D897")
    ativos_o2 = api.get_ativos()


    if request.method == "POST":
        hoje = datetime.strptime(request.POST['data'], "%Y-%m-%d")


    eventos = get_all_events_api(hoje) 

    for item in eventos:
        dados_o2 = get_emissor(ativos_o2 , item['titulo'])
        item['emissor'] =  dados_o2['nomeEmissor']
        try:
            item['dtfim'] = datetime.strptime(dados_o2['dataFimRelacionamento'][0:10] , "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            item['dtfim'] =  "00/00/0000"
    dados  = {
        "dia":  hoje.strftime("%d/%m/%Y") ,
        "eventos" : eventos  ,
        # "diautil" : CalculoDiaUtil(hoje).calculardiautil() ,
        # "ativos":   ativos
    }
    return render(request , "eventos/home.html" , dados)



def baixar_eventos_excel(request):

    hoje = datetime.today()

    api =  o2Api("thiago.conceicao","DBCE0923-9CE3-4597-9E9A-9EAE7479D897")
    ativos_o2 = api.get_ativos()



    eventos = get_all_events_api(hoje) 

    for item in eventos:
        dados_o2 = get_emissor(ativos_o2 , item['titulo'])
        item['emissor'] =  dados_o2['nomeEmissor']
        try:
            item['dtfim'] = datetime.strptime(dados_o2['dataFimRelacionamento'][0:10] , "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            item['dtfim'] =  "00/00/0000"




    filename = f"eventos_diarios.xlsx"
    dataframes = pd.DataFrame.from_dict(eventos)
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            dataframes.to_excel(writer, sheet_name="eventos_diarios", index=False)
            return res




def excluir_ativo(request):

    ativo  =  request.GET['ativo']

    con = engine.connect()
    con.execute(text(f"delete from pmts where Título='{ativo}' "))
    con.commit()
    return redirect('ativoscomeventos')



def detalhe_ativos(request):
    ativo = request.GET['ativo']
    dados_ativo = get_all_events_ativo(ativo)
    dados = {
        "eventos": dados_ativo , 
        "ativo": ativo
    }

    return render(request , "eventos/cadastroAtivos.html" , dados)





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
