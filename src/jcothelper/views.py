from django.shortcuts import render
from django.http import request,HttpRequest , HttpResponse
from django.shortcuts import get_object_or_404
from .helper_class import BuscarPosicaoJcot
from .models import PosicaoFundoJcot
from JCOTSERVICE import ListFundosService
import pandas as pd
import csv
from io import BytesIO
from datetime import datetime
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
    fundos['dataPosicao'] = fundos['dataPosicao'].apply(lambda x : datetime.strptime(x , "%Y-%m-%d"))
    filename = f"fundos.xlsx"
    with BytesIO() as b:
        res = HttpResponse(
            b.getvalue(),  # Gives the Byte string of the Byte Buffer object
            content_type="application/xlsx",
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        with pd.ExcelWriter(res) as writer:
            fundos.to_excel(writer, sheet_name="fundos", index=False)
            return res



def buscar_posicoes_jcot(request):
   posicoes_jcot  = BuscarPosicaoJcot()
   df = posicoes_jcot.buscar_fundos()
   print (df)
   return render(request, "jcothelper/homepage.html" )
