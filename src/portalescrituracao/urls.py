"""portalescrituracao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from listfundos.views import  *
from eventosapp.urls import *
from jcothelper.urls import *
from zapemissoresApp.urls import *
from emissoresapp.urls import *
from .views import homepage
from conciliacao.urls import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("listar" , listarfundos ) ,
    path("" , homepage ,  name = "pagina_inicial" ) ,
    path("eventos/" , include("eventosapp.urls") ) , 
    path("jcothelper/" , include("jcothelper.urls") ) , 
    path("zapemissores/" , include("zapemissoresApp.urls")) , 
    path("emissores/" , include("emissoresapp.urls")) ,
    path("xpapp/" , include("xpapp.urls")) ,  
    path("conciliacao/" , include("conciliacao.urls")) ,
    path("sqdados/" , include("sqdados.urls"))


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
