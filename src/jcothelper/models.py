from django.db import models

# Create your models here.



class PosicaoFundoJcot(models.Model):
    id = models.BigAutoField(primary_key=True)
    cd_fundo = models.CharField(max_length=15)
    quantidade = models.FloatField()
    quantidade_maps = models.FloatField(default=0)
    descricao = models.CharField(max_length=250 , default="")
