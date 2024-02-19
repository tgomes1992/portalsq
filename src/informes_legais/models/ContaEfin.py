from django.db import models
from datetime import datetime



class ContaEfin(models.Model):
    creditos = models.FloatField()
    debitos = models.FloatField()
    principal = models.FloatField(default=0)
    creditosmsmtitu = models.FloatField()
    debitosmsmtitu = models.FloatField()
    # principal no último dia do mês
    vlrultidia = models.FloatField()
    fundoCnpj = models.CharField(max_length=14)
    numconta = models.TextField(max_length=14)
    data_final = models.DateTimeField(default=datetime.now())

