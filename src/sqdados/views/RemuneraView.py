from django.shortcuts import render , redirect
from ..controllers.RemuneraController import RemuneraController
from ..controllers.CalculoReceitas import CalculoRemunera


# Create your views here.




def home_remuneracao(request):
    return render(request, "sqdados/remuneracao.html")


def atualizar_codigos_ot(request):
    RemuneraController().get_cds_ot()
    return redirect('remuneracao')



def importar_arquivo_remunera(request):
    if request.method ==  'POST':
        arquivo = request.FILES['arquivo']
        calculo = CalculoRemunera(arquivo)
        calculo.read_file()
    return redirect('remuneracao')
