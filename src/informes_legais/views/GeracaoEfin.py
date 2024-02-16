from django.views import View
from django.shortcuts import render
from django.http import HttpResponse ,  JsonResponse
from ..ControllersEfinanceira import *
from ..models import ContaEfin , InvestidorEfin
from JCOTSERVICE import ListFundosService
import os


class GeracaoEfin(View):


    def extracao_efinanceira(self):
        service_extracao = ExtratorMovimentacoes()
        fundos = ListFundosService(os.environ.get("JCOT_USER") ,
                                     os.environ.get("JCOT_PASSWORD")).listFundoRequest()
        fundos_dtvm = fundos[fundos['administrador'] ==  '36113876000191']
        
        # extracao = [{
        #     'cd_fundo':  "1944" ,
        #     'data_inicial':  "2023-12-01",
        #     'data_final':  "2023-12-31" ,
        #     "cnpj_fundo": "17455369000191"
        # }]

        extracao = [{
            'cd_fundo':  item['codigo'] ,
            'data_inicial':  "2023-11-01",
            'data_final':  "2023-11-30" ,
            "cnpj_fundo": item['cnpj']
        } for item in fundos_dtvm.to_dict("records")]

        for item in extracao:
            service_extracao.base_movimentacoes(item)


    def CriarContas(self):
        '''buscar dados dos investidores'''
        contas = ContaEfin.objects.values('numconta').distinct()
        cotistas = []
        for item in contas:
            consulta = item['numconta'].split("|")[0].strip()[0:13]
            print (consulta)
            investidor = InvestidorEfin(cpfcnpj = consulta )
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
        investidores = InvestidorEfin.objects.all()        

        for investidor in investidores:
            print (investidor.cpfcnpj)
            geracao = GeradorEfinanceira(investidor.cpfcnpj , investidor.nome , investidor.endereco , investidor.pais , datetime(2023,11,30))
            geracao.gerar_arquivo_efin()
        pass

    def get(self, request):
        #todo incluir depois a possibilidade de receber
        # uma lista de fundos para ser a base da extração

        # self.rotinas_pre_arquivos()

        self.MontarArquivos()


        return JsonResponse({"message":"Extração Iniciada"})