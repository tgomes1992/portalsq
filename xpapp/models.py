from django.db import models
from datetime import datetime
# Create your models here.


class FundoXP(models.Model):
    o2id = models.BigIntegerField(default=0)
    nome = models.CharField(max_length=200)
    cd_jcot = models.CharField(max_length=15 , primary_key=True)
    cnpj = models.CharField(max_length=14)
    categoria =  models.CharField(max_length=200 , default="catxp")

    def __str__(self):
        return self.nome

class InvestidoresXp(models.Model):
    NO_CGC = models.CharField(max_length=15 , default=0)
    CD_CLIENTE  = models.CharField(max_length=15)
    NM_CLIENTE = models.CharField(max_length=200)
    IC_FJ_PESSOA = models.CharField(default=0 , max_length=2)
    DATA = models.DateTimeField()
    C_ORDEM = models.CharField(max_length=3)
    tipo_cotista = models.IntegerField(default=0)
    statusJcot = models.BooleanField()
    status_cadastro_cotista = models.BooleanField(default=0)

    def cliente_dados_cadastro(self):
        return {
            'codigo':  self.CD_CLIENTE ,
            "tipo": self.IC_FJ_PESSOA ,
            "nome": self.NM_CLIENTE ,
            "cnpj": self.NO_CGC ,
            "codigo": self.CD_CLIENTE ,
         }


    def cotista_dados_cadastro(self):
        return {
            'cd_cliente' : self.CD_CLIENTE ,
            'tipo_cotista': self.tipo_cotista ,
            'c_ordem': "S" ,
        }

class MovimentacoesXP(models.Model):
    cd_investidor = models.CharField(max_length=200)
    cd_fundo = models.CharField(max_length=15)
    tipo_movimentacao = models.CharField(max_length=15 , default="A")
    data_movimentacao = models.DateTimeField(default=datetime.today())
    valor = models.FloatField()
    filename = models.CharField(max_length=400)
    statusJcot = models.BooleanField(default=False)


    def movimentos_base_df(self):
        return {
            "cd_investidor": self.cd_investidor,
            "cd_fundo": self.cd_fundo,
            "tipo_movimentacao": self.tipo_movimentacao,
            "data_movimentacao": self.data_movimentacao,
            "valor":  self.valor,
            "filename":  self.filename,
            "statusJcot": self.statusJcot,
        }





    def depara_fundos(self ,  tp):
        # fundos = {
        #   '49983891000132': "49321" ,
        #    "43121036000136": "30991"
        # }

        fundos = FundoXP.objects.filter(cnpj=tp).first().cd_jcot
        return fundos

    def depara_tipo_movimentacao(self,tp):
        depara =  {
            "A":"A" ,
            "RT":"RT" ,
            "RP": "RB"
        }
        return depara[tp]

    def registro_lancamento(self):
        return {
            "data": self.data_movimentacao.strftime("%Y-%m-%d"),
            "tipo": self.depara_tipo_movimentacao(self.tipo_movimentacao),
            "cotista": self.cd_investidor,
            "fundo": self.depara_fundos(self.cd_fundo) ,
            "liquidacao": "LI",
            "valor": self.valor,
            "qtdcotas": 0
        }


class ArquivosXp(models.Model):
    filename = models.CharField(max_length=400)
    filedate = models.CharField(max_length=8)

    def ajustar_dia_arquivo(self):
        return self.filename.split("_")[4]