from django.shortcuts import render
from ..forms import ArquivosForm

# Create your views here.


def analise_5401(request):
    form = ArquivosForm()

    context = {
        "form":  form,
    }

    return render(request ,"informes_legais/analise_5401.html" , context)



def analise_efinanceira(request):
    form = ArquivosForm()

    context = {
        "form":  form,
    }
    return render(request ,"informes_legais/analise_efinanceira.html" , context)

