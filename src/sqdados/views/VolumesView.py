from django.shortcuts import render , redirect
from ..controllers.VolumesController import VolumesController
from ..controllers.ArquivoDconciliacao import LeituraArquivoDconciliacao
from ..models import ArquivoDconciliacao
# Create your views here.
from io import BytesIO
from datetime import datetime
from ..controllers.ArquivoSecurityList import ImportacaoSecureClient
from ..controllers.VolumesController import VolumesController
import pandas as pd


def home_volumes(request):
    controle_volumes = VolumesController()   
    return render(request, "sqdados/volumes.html")


def importacao_arquivo_dconciliacao(request):
    if request.method == "POST":
        ## lógica de importação do arquivo
        leitor = LeituraArquivoDconciliacao() 
        resultado = leitor.leitura_arquivo(request.FILES['arquivo']).to_dict('records')
        for item in resultado:
            if item['data'] !=  "":
                file_line = ArquivoDconciliacao(
                    data = datetime.strptime(item['data'], "%Y%m%d") ,
                    tipo_ativo = item['tipo_ativo'] , 
                    ativo = item['ativo'] ,
                    quantidade = item['quantidade']                
                )
                if not ArquivoDconciliacao.objects.filter(data = file_line.data , 
                                                      tipo_ativo = file_line.tipo_ativo , 
                                                      ativo = file_line.ativo , 
                                                      quantidade  =  file_line.quantidade).first():
                    file_line.save()


    return redirect('volumes')

def importar_arquivo_securityList(request):
    if request.method ==  'POST':
        arquivo = request.FILES['arquivo']
        secure_client_importacao = ImportacaoSecureClient()
        secure_client_importacao.importar_arquivo(arquivo)       
    return redirect('volumes')


def processar_volumes(request):
    VolumesController().processar_volumes().to_csv("volumes.csv")
    return redirect("volumes")
