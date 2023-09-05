


# @app.route("/main",methods=['POST','GET'])
# def main():    
#     if request.method == "POST":
#         data = datetime.strptime(request.form['datasaldo'],"%Y-%m-%d")    
#         df = ControllerZAP().get_saldos(data)
#         dataexcel = data
#     else:
#        df = ControllerZAP().get_saldos(datetime.today())
#        dataexcel = datetime.today()
#     dados = {
#         "saldos": df.sort_values(by=['ValorSaldoTotal'], ascending=False).to_dict("records")
#     }
#     return render_template("base.html" , data=dados)




# @app.route("/downloadexcel")
# def download_excel():
#     data = request.args.get("data")
#     data_formatado =  datetime.strptime(data,"%Y-%m-%d")
#     df = ControllerZAP().get_saldos(data_formatado)
#     df.to_excel("dataexcel.xlsx")
#     return send_file("dataexcel.xlsx")
#     # return redirect(url_for("main"))




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
from zapemissoresApp.views import *






urlpatterns = [
    path('', main_emissores  ,  name="home_zap_emissores"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
