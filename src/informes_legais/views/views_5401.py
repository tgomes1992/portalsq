from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from ..forms import ArquivosForm
from io import BytesIO
import pandas as pd
from ..validacao_5401 import XML_5401



class View_5401(View):

    template_name = "informes_legais/analise_5401.html"
    form = ArquivosForm()

    def get(self, request):
        context = {
            "form": self.form,
        }

        return render(request ,self.template_name , context)

    def post(self , request):
        filename = "analise_5401.xlsx"
        arquivo = request.FILES['arquivo']
        with BytesIO() as b:
            res = HttpResponse(
                b.getvalue(),  # Gives the Byte string of the Byte Buffer object
                content_type="application/xlsx",
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
            xml_5401 = XML_5401(arquivo)
            xml_5401.gerar_arquivo_validacao(res)

        return res
