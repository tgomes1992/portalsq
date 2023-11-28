
# Create your models here.


from django.db import models 
from django.db.models import Model 
# Create your models here. 
  
class DiFator(Model): 
    data = models.DateTimeField()
    fator = models.FloatField()
    selic = models.FloatField()
