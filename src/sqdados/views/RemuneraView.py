from django.shortcuts import render , redirect
from django.core.paginator import Paginator
from ..controllers.RemuneraController import RemuneraController
from ..controllers.CalculoReceitas import CalculoRemunera
import pandas as pd
from ..models import ReceitaMensal
from ..forms import ReceitaMensalForm , ReceitaRelatorios , ProcessarReceita

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


def cadastrar_nova_remuneracao(request):
    if request.method == 'POST':
        form = ReceitaMensalForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to a success page or any other desired page
            return redirect('success_page')
        # If the form is not valid, re-render the form with error messages
    else:
        # If it's a GET request, create a new form
        form = ReceitaMensalForm()

    return render(request, 'sqdados/CadastroRemuneracao.html', {'form': form})

def relatorios_remuneracao(request):

    form1 = ReceitaRelatorios()
    form2 = ProcessarReceita()


    return render(request, 'sqdados/RelatoriosReceita.html', {'form1': form1 , 'form2':form2})