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
        
        extracao = [
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-01-01",
            'data_final':  "2023-01-31" ,
            "cnpj_fundo": "17455369000191" , 
            'tipo_fundo':  'FIM ABERTO'
        } , 
            
        {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-02-01",
            'data_final':  "2023-02-28" ,
            "cnpj_fundo": "17455369000191" , 
            'tipo_fundo':  'FIM ABERTO'
        } , 
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-03-01",
            'data_final':  "2023-03-31" ,
            "cnpj_fundo": "17455369000191" ,
            'tipo_fundo':  'FIM ABERTO'
        } , 
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-04-01",
            'data_final':  "2023-04-30" ,
            "cnpj_fundo": "17455369000191" ,
            'tipo_fundo':  'FIM ABERTO'
        },  {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-05-01",
            'data_final':  "2023-05-31" ,
            "cnpj_fundo": "17455369000191" ,
            'tipo_fundo':  'FIM ABERTO'
        },
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-06-01",
            'data_final':  "2023-06-30" ,
            "cnpj_fundo": "17455369000191"  , 
            'tipo_fundo':  'FIM ABERTO'
        } ,
             {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-07-01",
            'data_final':  "2023-07-31" ,
            "cnpj_fundo": "17455369000191" , 
            'tipo_fundo':  'FIM ABERTO'
        } ,  
        {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-08-01",
            'data_final':  "2023-08-31" ,
            "cnpj_fundo": "17455369000191" ,
            'tipo_fundo':  'FIM ABERTO'
        },
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-09-01",
            'data_final':  "2023-09-30" ,
            "cnpj_fundo": "17455369000191" , 
            'tipo_fundo':  'FIM ABERTO'
        } ,    
          {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-10-01",
            'data_final':  "2023-10-31" ,
            "cnpj_fundo": "17455369000191"
        } ,
            {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-11-01",
            'data_final':  "2023-11-30" ,
            "cnpj_fundo": "17455369000191" , 
            'tipo_fundo':  'FIM ABERTO'
        } , {
            'cd_fundo':  "1944" ,
            'data_inicial':  "2023-12-01",
            'data_final':  "2023-12-31" ,
            "cnpj_fundo": "17455369000191" ,
            'tipo_fundo':  'FIM ABERTO'
        }]

        # extracao = [{
        #     'cd_fundo':  item['codigo'] ,
        #     'data_inicial':  "2023-11-01",
        #     'data_final':  "2023-11-30" ,
        #     "cnpj_fundo": item['cnpj']
        # } for item in fundos_dtvm.to_dict("records")]

        
        # extracao = [{
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-01-01",
        #     'data_final':  "2023-01-31" ,
        #     "cnpj_fundo": "28819553000190"
        # } ,  {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-02-01",
        #     'data_final':  "2023-02-28" ,
        #     "cnpj_fundo": "28819553000190"
        # } , {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-03-01",
        #     'data_final':  "2023-03-31" ,
        #     "cnpj_fundo": "28819553000190"
        # } , {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-04-01",
        #     'data_final':  "2023-04-30" ,
        #     "cnpj_fundo": "28819553000190"
        # } , {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-05-01",
        #     'data_final':  "2023-05-31" ,
        #     "cnpj_fundo": "28819553000190"
        # } ,  {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-06-01",
        #     'data_final':  "2023-06-30" ,
        #     "cnpj_fundo": "28819553000190"
        # } , {
        #     'cd_fundo':  "38281_SEN01" ,
        #     'data_inicial':  "2023-07-01",
        #     'data_final':  "2023-07-31" ,
        #     "cnpj_fundo": "28819553000190"
        # } ]

        
        for item in extracao:
            service_extracao.base_movimentacoes(item)


    def CriarContas(self):
        '''buscar dados dos investidores'''
        contas = ContaEfin.objects.values('numconta').distinct()
        cotistas = []
        for item in contas:
            consulta = item['numconta'].split("|")[0].strip()
            print (consulta)
            investidor = InvestidorEfin(cpfcnpj = consulta )
            investidor.save()

    def AtualizarInvestidores(self):
        service_atualiza_investidores = AtualizacaoInvestidores()
        # service_atualiza_investidores.atualizar_enderecos()
        service_atualiza_investidores.atualizar_enderecos_busca_o2()        
        service_atualiza_investidores.atualizar_nomes()

    def rotinas_pre_arquivos(self):
        '''rotina da efinanceira pre_geracao de arquivos'''
        self.extracao_efinanceira()
        self.CriarContas()
        # self.AtualizarInvestidores()

    def MontarArquivos(self):
        investidores = InvestidorEfin.objects.all()        

        for investidor in investidores:
            print (investidor.cpfcnpj)
            geracao = GeradorEfinanceira(investidor.cpfcnpj , investidor.nome , investidor.endereco , investidor.pais , datetime(2023,7,31))
            geracao.gerar_arquivo_efin()
        pass

    def get(self, request):
        #todo incluir depois a possibilidade de receber
        # uma lista de fundos para ser a base da extração

        self.rotinas_pre_arquivos()

        self.MontarArquivos()

        # dados = {
        #     'cotista': '14665341000190' , 
        #     'data':  '2023-12-29'
        # }

        # d = BuscaPrincipalJcot().get_dados_principal_por_cotista(dados)

        # print(d)


        return JsonResponse({"message":"Extração Iniciada"})