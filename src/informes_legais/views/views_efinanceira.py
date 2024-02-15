from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from ..forms import ArquivosForm

class View_Efinanceira(View):
    template_name = "informes_legais/analise_efinanceira.html"
    form = ArquivosForm()

    def get(self, request):
        context = {
            "form": self.form,
        }

        return render(request, self.template_name, context)