from django.views import View
from django.shortcuts import render
from django.http import HttpResponse ,  JsonResponse
from ..ControllersEfinanceira import ExtratorMovimentacoes , ExtratorPrincipalJcot
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


    def MontagemEfinanceira(self):
        '''buscar dados dos investidores'''
        contas = ContaEfin.objects.values('numconta').distinct()
        cotistas = []
        for item in contas:
            investidor = InvestidorEfin(cpfcnpj = item['numconta'].split("|")[0].strip())
            investidor.save()





    def get(self, request):
        #todo incluir depois a possibilidade de receber
        # uma lista de fundos para ser a base da extração

        # self.extracao_efinanceira()

        self.MontagemEfinanceira()

        return JsonResponse({"message":"Extração Iniciada"})