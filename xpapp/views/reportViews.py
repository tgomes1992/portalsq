from django.shortcuts import render
from django.http import HttpResponse


def relatorios_diarios_xp(request):
    return render(request,"xpapp/relatorios_diarios_xp.html")
