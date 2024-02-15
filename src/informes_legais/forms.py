from django import forms


class ArquivosForm(forms.Form):

    arquivo = forms.FileField()


class ExtracaoEfin(forms.Form):
    OPTIONS = [
        ('movimentacao', 'Arquivo de Movimentação',),
        ('posicao', 'Arquivo de Posição',),
        ('posicao_geral', 'Posição Consolidada',),
    ]

    tipoarquivo = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'select'}),  # Add any additional attributes or classes here
    )