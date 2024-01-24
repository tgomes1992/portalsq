from django import forms
from .models import FundoXP


class RelatoriosDiariosXP(forms.Form):
    OPTIONS = [
        ('movimentacao' ,'Arquivo de Movimentação', ),
        ( 'posicao' , 'Arquivo de Posição', ),
        (  'posicao_geral','Posição Consolidada', ),
    ]

    tipoarquivo = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'select'}),  # Add any additional attributes or classes here
    )

    data = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))
    


class ImportacaoArquivosDiarios(forms.Form):
    OPTIONS = [
        ('Arquivo Diário - XP' ,'diariopco' ),

    ]
    arquivo = forms.FileField()




class ProcessarMovimentacoes(forms.Form):
    OPTIONS = [(fundo.cnpj , fundo.nome) for fundo in FundoXP.objects.all() ]
    OPTIONS.append(("Selecione o fundo a ser importado","Selecione o fundo a ser importado"))
    OPTIONS.reverse()
    # fundo = forms.ChoiceField(
    #     choices=OPTIONS,
    #     widget=forms.Select(attrs={'class': 'select'}),  # Add any additional attributes or classes here
    # )

    dataMovimentacoes = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))



class PCOS_LOTE(forms.Form):
    OPTIONS = [
        ('' ,'Selecione o Tipo de Importação', ),
        ( 'diariopco' , "Pcos em Lote", )
    ]

    tipoarquivo = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'select'}),  # Add any additional attributes or classes here
    )

    arquivo = forms.FileField()

