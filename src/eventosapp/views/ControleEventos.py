from django.shortcuts import render , redirect
from django.http import request , HttpRequest , HttpResponse , JsonResponse
from ..models import EventosDiarios
import json
from intactus import o2Api
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def get_emissor(ativos_o2 , codigo):

    try:
        return ativos_o2[ativos_o2['codigo'] == codigo ].to_dict("records")[0]
    except Exception as e:
        return {
            "nomeEmissor": 'na' , 
            "dataFimRelacionamento": "na"
        }


@csrf_exempt
def AdicionarEventosDiarios(request):
    api =  o2Api("thiago.conceicao","DBCE0923-9CE3-4597-9E9A-9EAE7479D897")
    # ativos_o2 = api.get_ativos()

    if request.method == "POST":
        eventos = json.loads(request.body)
        

        for item in eventos:
            evento = EventosDiarios(ativo =item['Título'] , 
                                    emissor = "na" , 
                                    data_base =  datetime.strptime(item['Data Original'] , 
                                                                   "%d/%m/%Y") , 
                                    data_liquidacao = datetime.strptime(item['Data de Liquidação'] ,  
                                                                        "%d/%m/%Y")
                                    )
            trava_salvamento = EventosDiarios.objects.filter(ativo = evento.ativo , 
                                                           data_base = evento.data_base ,  
                                                           data_liquidacao = evento.data_liquidacao).first()
            if not trava_salvamento:
                evento.save()

    # print (eventos)

    return JsonResponse({"message": "Eventos Importados com sucesso"})


