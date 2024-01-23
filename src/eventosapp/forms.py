from django import forms



class PeriodoEspecifico(forms.Form):
    data = forms.DateField(widget=forms.Select(attrs={'class': 'datepicker'}))
    
