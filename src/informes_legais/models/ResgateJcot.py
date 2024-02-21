from django.db import models




class ResgatesJcot(models.Model):
    '''classe que vai ser a base das movimentações e geracao do debito e credito de cada um dos cotistas'''
    data_movimento = models.DateTimeField()
    data_liquidacao = models.DateTimeField()
    nota = models.CharField(max_length = 50 , default=" " , primary_key=True)
    cd_tipo = models.CharField(max_length=20, default=" ")
    cd_cotista = models.CharField(max_length=16 ,  default = " ")        
    cd_fundo = models.TextField()
    # codigo no qual ocorreu a movimentacao    
    vl_original = models.FloatField()
    vl_liquido = models.FloatField()
    vl_bruto = models.FloatField()