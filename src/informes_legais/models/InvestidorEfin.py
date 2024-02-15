from django.db import models
from datetime import date, datetime

class InvestidorEfin(models.Model):
    nome = models.CharField(max_length=256 ,  default="")
    cpfcnpj = models.CharField(max_length=14 ,  default="" , primary_key=True )
    endereco = models.TextField(max_length=256 ,  default="")
    #pais vai ser sempre abreviação
    pais = models.TextField(max_length=5 , default="")
