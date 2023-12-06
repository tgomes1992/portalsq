from django.shortcuts import render
from ..controllers.VolumesController import VolumesController

# Create your views here.





def home_volumes(request):
    controle_volumes = VolumesController()
    datas = controle_volumes.get_codigos_ot_o2()
    datas.to_excel("ativos.xlsx", index=False)


    
    return render(request, "sqdados/volumes.html")
