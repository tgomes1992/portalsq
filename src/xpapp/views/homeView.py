from django.shortcuts import render
from django.http import HttpResponse


def home_page_xp_app(request):
    return render(request,"xpapp/home_xp_app.html")



