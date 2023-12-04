
from django.shortcuts import render
from ..controllers.Quantitativoo2 import *
from datetime import datetime




def home_quantitativo(request):
    return render(request, "sqdados/quantitativo.html")



def list_fundos_ativos(request):
    data  = datetime(2023,3,31)
    fundos_ativos = CalculoQuantitativoO2(data).get_fundos_ativos()
    fundos_ativos.to_excel("fundos.xlsx")
    return render(request, "sqdados/quantitativo.html")


def list_outros_ativos(request):
    data  = datetime(2023,3,31)
    fundos_ativos = CalculoQuantitativoO2(data).get_outros_ativos_ativos()
    fundos_ativos.to_excel("outros_ativos.xlsx")
    return render(request, "sqdados/quantitativo.html")