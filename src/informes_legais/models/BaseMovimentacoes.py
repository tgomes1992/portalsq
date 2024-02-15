from django.db import models


class BaseMovimentacoes(models.Model):
    '''classe que vai ser a base das movimentações e geracao do debito e credito de cada um dos cotistas'''
    data = models.DateTimeField()
    cd_tipo = models.CharField(max_length=20, default=" ")
    # codigo no qual ocorreu a movimentacao
    cd_jcot = models.TextField()
    cotista = models.TextField()
    vl_original = models.FloatField()
    vl_liquido = models.FloatField()
    vl_bruto = models.FloatField()