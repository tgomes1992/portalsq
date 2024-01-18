# Create your models here.
from django.db import models
from django.db.models import Model


# Create your models here.

class ReceitaMensal(Model):
    PERIODICIDADE = [
        ('Mensal', 'Mensal'),
        ('Anual', 'Anual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
    ]
    cd_ot = models.CharField(max_length=20)
    periodicidade = models.CharField( max_length=10, choices=PERIODICIDADE)
    valor_remuneracao = models.FloatField()
    emissor = models.CharField(max_length=250)
    emissor_cnpj = models.TextField(max_length=14)
    resumo_contrato = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo_ativo = models.CharField(max_length=25)


