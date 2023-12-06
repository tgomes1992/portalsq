from django.db import models

# Create your models here.



class FundoXP(models.Model):
    fundo = models.CharField(max_length=30)
    diaUtil = models.IntegerField()


class EventosDiarios(models.Model):
    ativo = models.CharField(max=200)
    emissor = models.CharField(max_length=250)
    data_base = models.DateTimeField()
    data_liquidacao = models.DateTimeField()




