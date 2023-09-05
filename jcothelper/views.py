from django.shortcuts import render
from django.http import request,HttpRequest , HttpResponse
from django.shortcuts import get_object_or_404
from .helper_class import BuscarPosicaoJcot
from .models import PosicaoFundoJcot
from JCOTSERVICE import ListFundosService
import pandas as pd
import csv
# Create your views here.

def homejcothelper(request):
   return render(request, "jcothelper/home_jcot_helper.html" )

def importacao_cadastros(request):
   return render(request, "jcothelper/importacao_xp.html"  )

def batimentos_home(request):
   posicoes = PosicaoFundoJcot.objects.all()
   return render(request, "jcothelper/batimentos.html" , {"posicoes": posicoes} )

def listfundosjcot(request):
   fundos = ListFundosService("roboescritura" , "Senh@123").listFundoRequest().to_dict("records")
   return render(request , 'jcothelper/list_fundos.html' , {"fundos": fundos})
   
def download(request):
    fundos = ListFundosService("roboescritura" , "Senh@123").listFundoRequest()
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="fundos.csv"'},
      )
    writer = csv.writer(response , delimiter=";" )
    writer.writerow(fundos.columns)
    for item in fundos.iterrows():
       writer.writerow(item[1].to_list())
    return response



def buscar_posicoes_jcot(request):
   posicoes_jcot  = BuscarPosicaoJcot()
   df = posicoes_jcot.buscar_fundos()
   print (df)
   return render(request, "jcothelper/homepage.html" )
