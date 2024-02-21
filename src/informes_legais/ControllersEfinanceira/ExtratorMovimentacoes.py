import requests
import pandas as pd
from ..models import BaseMovimentacoes  , ContaEfin , ResgatesJcot , MovimentoDetalhado
from JCOTSERVICE import RelAnaliticoCotistaFundo , ConsultaMovimentoPeriodoV2Service
import os
from datetime import datetime


class ExtratorMovimentacoes():
    service_movimentos = RelAnaliticoCotistaFundo(os.environ.get("JCOT_USER"),
                                                           os.environ.get("JCOT_PASSWORD"))
    
    service_buscar_resgates = ConsultaMovimentoPeriodoV2Service(os.environ.get("JCOT_USER"),
                                                           os.environ.get("JCOT_PASSWORD"))

    def buscar_movimentos(self, dados):
        movimentos = self.service_movimentos.get_movimento_periodo_request(dados)
        return movimentos

    def buscar_movimentos_detalhados(self,dados):
        movimentos = self.service_movimentos.get_movimentos_detalhados(dados)
        for item in movimentos:
            nmovimento = MovimentoDetalhado.from_dict(item)
            nmovimento.save()
        return movimentos


    def get_nota_principal(self,nota):
        nota = MovimentoDetalhado.objects.filter(notaOperacao = nota).first()
        return nota.vlOriginal


    def atualizar_principal_notas_resgate(self):
        resgates = ResgatesJcot.objects.filter(vl_original=0).all()
        for resgate in resgates:
            resgate.vl_original  =self.get_nota_principal(resgate.nota)
            resgate.save()


    def main_extrair_movimentacoes(self ,  dados):
        dados['movimento'] = "R"
        # self.base_movimentacoes(dados)
        # self.extrair_resgates(dados)
        # self.buscar_movimentos_detalhados(dados)
        self.atualizar_principal_notas_resgate()
     

    def base_movimentacoes(self, dados):
        contas = self.buscar_movimentos(dados)
        try:
            contas_efin_a_salvar = [ContaEfin(
                creditos = item['aplicacao_principal'],
                debitos = item['resgate_operacao'],
                principal = item['resgate_principal'],
                creditosmsmtitu = 0,
                debitosmsmtitu = 0,
                vlrultidia  = 0,
                fundoCnpj = dados['cnpj_fundo'],
                numconta = f"{item['cd_fundo']}|{item['cd_cotista']}",
                data_final = item['data_final']
            ) for item in contas]
            for item in contas_efin_a_salvar:
                item.save()
        except Exception as e:
            print (e)
            pass
    
    def extrair_resgates(self, dados):
        resgates = self.service_buscar_resgates.get_movimento_periodo_request(dados)
        try:
            resgates_a_salvar = [ResgatesJcot(
                data_movimento = item['dtMov'],
                data_liquidacao = item['dtLiqFinanceira'],
                nota = item['nota'],
                cd_tipo = item['cdTipoMov'],
                cd_cotista = item['cotista'],
                cd_fundo  = item['cdFundo'],
                vl_original = 0,
                vl_liquido = item['vlLiquido'],
                vl_bruto = item['vlBruto']
            ) for item in resgates]

            for item in resgates_a_salvar:
                print (item)
                item.save()
        except Exception as e:
            print (e)
            pass

    # def atualizar_principal(self,dados):
    #     movimentos = ResgatesJcot.objects.all()



    #     pass        



















