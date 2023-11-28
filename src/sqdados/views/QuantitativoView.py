
from django.shortcuts import render






def home_quantitativo(request):
    return render(request, "sqdados/quantitativo.html")
