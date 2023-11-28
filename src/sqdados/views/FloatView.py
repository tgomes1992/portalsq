from django.shortcuts import render
import pandas as pd 
from ..controllers.FloatDiario import ArquivoFloatDiario

# Create your views here.





def home_float(request):
    if request.method== 'POST':
        importador = ArquivoFloatDiario()
        base = importador.ImportarDi(request.FILES['arquivo'])



        
        # arquivo = request.FILES['floatDiario']

        # df = pd.read_csv(arquivo)

    return render(request, "sqdados/float.html")
