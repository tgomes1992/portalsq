from django import forms
import pandas as pd
from .app_control import Ativoso2Sinc

class ConciliacaoForm(forms.Form):

    dados = Ativoso2Sinc()

    # OPTIONS = dados.get_ativos_form()
    OPTIONS = []

    fundos = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'select'}),
    )

    data = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))