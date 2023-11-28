from django.db import models

# Create your models here.



class FundoXP(models.Model):
    fundo = models.CharField(max_length=30)
    diaUtil = models.IntegerField()