from django.shortcuts import render , redirect
from emissoresapp.models import *
from intactus.o2requests import IntactusRequests
# Create your views here.


def home_emissores_app(request):
    emissores = Emissor.objects.all()
    dados = {
        "emissores": emissores
    }

    return render(request, 'emissores/lista_emissores.html' , dados )





def cadastro_emails(request):
    emissores = Emissor.objects.all()
    dados = {
        "emissores": emissores
    }
    return render(request , 'emissores/cadastro_emails.html' ,  dados )



def o2sinc(request):
    requests_intactus = IntactusRequests()
    emissores = Emissor.objects.all()

    ids = [emissor.o2id for emissor in emissores]
    df = requests_intactus.emissores_intactus().to_dict("records")

    for item in df:
        if item['ID'] not in ids:
            emissor = Emissor(name= item['Nome'] , cnpj = item['CNPJ'] ,  o2id = item['ID'])
            emissor.save()

    return redirect('/emissores')