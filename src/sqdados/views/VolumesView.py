from django.shortcuts import render

# Create your views here.







def home_volumes(request):
    return render(request, "sqdados/volumes.html")
