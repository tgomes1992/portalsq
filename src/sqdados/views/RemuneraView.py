from django.shortcuts import render , redirect
from django.core.paginator import Paginator
from ..controllers.RemuneraController import RemuneraController
from ..controllers.CalculoReceitas import CalculoRemunera
import pandas as pd
from ..models import ReceitaMensal

# Create your views here.


def home_remuneracao(request):
    return render(request, "sqdados/remuneracao.html")


def atualizar_codigos_ot(request):
    RemuneraController().get_cds_ot()
    return redirect('remuneracao')


def importar_arquivo_remunera(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        df = pd.read_excel(arquivo)

        calculo = CalculoRemunera(arquivo)
        calculo.read_file()
    return redirect('remuneracao')


def remuneracoes_ativas(request):
    remuneracoes = ReceitaMensal.objects.all()
    paginator = Paginator(remuneracoes , 10)
    page = request.GET.get("page")
    files_on_page = paginator.get_page(page)  

    return render(request ,  "sqdados/remuneracoes_ativas.html",  {"remuneracoes": files_on_page})