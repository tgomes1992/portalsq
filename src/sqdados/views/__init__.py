from django.shortcuts import render
from .FloatView import *
from .QuantitativoView import *
from .RemuneraView import *
from .VolumesView import *



def home_sq_dados(request):
    return render(request, "sqdados/home_sq_dados.html")
