import requests
import pandas as pd
from ..models import BaseMovimentacoes  , ContaEfin
from JCOTSERVICE import RelAnaliticoCotistaFundo
import os
from datetime import datetime


class ExtratorMovimentacoes():
    service_movimentos = RelAnaliticoCotistaFundo(os.environ.get("JCOT_USER"),
                                                           os.environ.get("JCOT_PASSWORD"))

    def buscar_movimentos(self , dados):
        movimentos = self.service_movimentos.get_movimento_periodo_request(dados)
        return movimentos

    def base_movimentacoes(self, dados):
        contas = self.buscar_movimentos(dados)

        try:
            contas_efin_a_salvar = [ContaEfin(
                creditos = item['aplicacao_principal'],
                debitos = item['resgate_operacao'],
                principal = item['resgate_principal'] , 
                creditosmsmtitu = 0,
                debitosmsmtitu = 0,
                vlrultidia  = 0,
                fundoCnpj = dados['cnpj_fundo'],
                numconta = f"{item['cd_fundo']}|{item['cd_cotista']}" ,
                data_final = item['data_final']
            ) for item in contas]
            for item in contas_efin_a_salvar:
                item.save()
        except Exception as e:
            print (e)
            pass


















