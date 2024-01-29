from django import forms



class ArquivosForm(forms.Form):

    arquivo = forms.FileField()
