from django.shortcuts import render

# Create your views here.



def analise_5401(request):
    return render(request ,"informes_legais/analise_5401.html")



def analise_efinanceira(request):
    return render(request ,"informes_legais/analise_efinanceira.html")