from django.shortcuts import render

# Create your views here.



def home_sq_dados(request):
    return render(request, "/sqdados/home_sq_dados.html")