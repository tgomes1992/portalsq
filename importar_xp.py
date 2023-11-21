from django.conf import settings
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalescrituracao.settings')
application = get_wsgi_application()
from xpapp.xphelper import ControleImportacaoArquivoDiario


    


arquivos_passivo = os.listdir('movimentacoes_xp\PASSIVO')


for file in arquivos_passivo:
    try:
        path_file = os.path.join('movimentacoes_xp\PASSIVO' , file)
        arquivo = ControleImportacaoArquivoDiario(path_file ,  file)
        arquivo.get_file_data()
    except Exception as e:
        print (file)
        print (e)


