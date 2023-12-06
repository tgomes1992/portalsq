
# Create your models here.


from django.db import models 
from django.db.models import Model 
# Create your models here. 
  
class DiFator(Model): 
    data = models.DateTimeField()
    fator = models.FloatField()
    selic = models.FloatField()



class FloatDiario(Model):
    ativo = models.CharField(max_length=250)
    data = models.DateTimeField()
    valor = models.FloatField()




class CDOT(Model):
    cd_ot = models.CharField(max_length=10)
    tipo_ativo = models.CharField(max_length=20)
    


# class Remunera(Model):
#     pass