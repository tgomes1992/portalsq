from django.shortcuts import render , redirect
from ..controllers.RemuneraController import RemuneraController


# Create your views here.






def home_remuneracao(request):
    return render(request, "sqdados/remuneracao.html")


def atualizar_codigos_ot(request):
    RemuneraController().get_cds_ot()
    return redirect('remuneracao')