from django.views import View
from django.shortcuts import render
from django.http import HttpResponse ,  JsonResponse
from ..ControllersEfinanceira import *
from ..models import ContaEfin , InvestidorEfin


class GeracaoEfin(View):


    def extracao_efinanceira(self):
        service_extracao = ExtratorMovimentacoes()
        extracao = [{
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-10-01",
            'data_final':  "2023-10-31" ,
            "cnpj_fundo": "17455369000191"
        }]
        for item in extracao:
            service_extracao.base_movimentacoes(item)


    def CriarContas(self):
        '''buscar dados dos investidores'''
        contas = ContaEfin.objects.values('numconta').distinct()
        cotistas = []
        for item in contas:
            investidor = InvestidorEfin(cpfcnpj = item['numconta'].split("|")[0].strip())
            investidor.save()

    def AtualizarInvestidores(self):
        service_atualiza_investidores = AtualizacaoInvestidores()
        service_atualiza_investidores.atualizar_enderecos()
        service_atualiza_investidores.atualizar_nomes()

    def rotinas_pre_arquivos(self):
        '''rotina da efinanceira pre_geracao de arquivos'''
        self.extracao_efinanceira()
        self.CriarContas()
        self.AtualizarInvestidores()

    def MontarArquivos(self):

        pass

    def get(self, request):
        #todo incluir depois a possibilidade de receber
        # uma lista de fundos para ser a base da extração

        # self.rotinas_pre_arquivos()

        self.MontarArquivos()


        return JsonResponse({"message":"Extração Iniciada"})