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
from django.http import HttpResponse
import zipfile
import os

def home_volumes(request):
    controle_volumes = VolumesController()   
    return render(request, "sqdados/volumes.html")


def unzip_file(zip_file_path):
    """
    Unzips a zip file to the specified directory.

    Parameters:
    - zip_file_path (str): Path to the zip file.
    - extract_to (str): Directory where the contents will be extracted.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('upload/imports')



def importacao_arquivo_dconciliacao(request):
    if request.method == "POST":
        ## lógica de importação do arquivo
        uploaded_file =  request.FILES['arquivo']

        if ".zip" in request.FILES['arquivo'].name:
              with open(os.path.join('upload', uploaded_file.name), 'wb') as destination:
                # Iterate over the uploaded file in chunks
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
      
              unzip_file(os.path.join('upload', uploaded_file.name))
              for arquivo in os.listdir('upload/imports'):
                leitor = LeituraArquivoDconciliacao() 
                resultado = leitor.leitura_arquivo_file_folder(os.path.join('upload/imports' , arquivo)).to_dict('records')
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
                #deleta o arquivo importado
                os.remove(os.path.join('upload/imports' , arquivo))
                    

        else:
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

        file = request.FILES['arquivo']

        if ".zip" in file.name:
            with open(os.path.join('upload', file.name), 'wb') as destination:
                # Iterate over the uploaded file in chunks
                for chunk in file.chunks():
                    destination.write(chunk)

            unzip_file(os.path.join('upload', file.name))

            for arquivo in os.listdir('upload/imports'):
                secure_client_importacao = ImportacaoSecureClient()
                secure_client_importacao.importar_arquivo(os.path.join( 'upload/imports', arquivo))
                os.remove(os.path.join( 'upload/imports', arquivo))


        else:
            arquivo = request.FILES['arquivo']
            secure_client_importacao = ImportacaoSecureClient()
            secure_client_importacao.importar_arquivo(arquivo)       
    
    
    return redirect('volumes')


def processar_volumes(request):
    volumes = VolumesController().processar_volumes()

    csv_data = volumes.to_csv(index=False)
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    return response



