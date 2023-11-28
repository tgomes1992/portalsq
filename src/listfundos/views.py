from django.shortcuts import render
from django.http import request,HttpRequest , HttpResponse
from .listfundosmodule import ListFundos
# Create your views here.


def listarfundos(request):
    fundos = ListFundos().listfundosrequest().to_dict("records")
    print (fundos)
    data = {
        'fundos':  fundos
    }
    return render(request, "listFundos.html" , data)


