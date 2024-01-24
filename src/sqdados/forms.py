from django import forms
from .models import ReceitaMensal




class ReceitaMensalForm(forms.ModelForm):
    class Meta:
        model = ReceitaMensal
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(attrs={'class': 'datepicker' }, format='%d/%m/%Y'),
            'data_fim': forms.DateInput(attrs={'class': 'datepicker'})
        }
        input_formats = ['%d/%m/%Y', '%Y-%m-%d' ,  "%m. %d , %Y"]


class ReceitaRelatorios(forms.Form):
    OPTIONS = [
        ('Receita por Ativo', 'Receita por Ativo'),
        ('Receita Mensal', 'Receita Mensal'),
        ('Remunerações Ativas', 'Remunerações Ativas'),
        ('remuneracoes_remunera', 'Remuneração Remunera'),
        ('remuneracoes_a_cadastrar', 'Remuneracoes a Cadastrar'),
    ]

    OPTIONS.append(("", "Selecione o Relatório"))

    OPTIONS.reverse()

    receita = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'select'}),  # Add any additional attributes or classes here
    )




class ProcessarReceita(forms.Form):


    periodo_inicial = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))
    
    periodo_final = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))