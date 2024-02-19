from django.views import View
from django.shortcuts import render
from django.http import HttpResponse ,  JsonResponse
from ..ControllersEfinanceira import *
from ..models import ContaEfin , InvestidorEfin
from JCOTSERVICE import ListFundosService
import os


class GeracaoEfin(View):

        
    def get_2023_year(self , cd_fundo, cnpj):
        
        extracao = [
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-01-01",
            'data_final':  "2023-01-31" ,
            "cnpj_fundo": cnpj ,             
        } , 
            
        {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-02-01",
            'data_final':  "2023-02-28" ,
            "cnpj_fundo": cnpj ,             
        } , 
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-03-01",
            'data_final':  "2023-03-31" ,
            "cnpj_fundo": cnpj ,            
        } , 
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-04-01",
            'data_final':  "2023-04-30" ,
            "cnpj_fundo": cnpj ,            
        },  {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-05-01",
            'data_final':  "2023-05-31" ,
            "cnpj_fundo": cnpj ,            
        },
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-06-01",
            'data_final':  "2023-06-30" ,
            "cnpj_fundo": cnpj  ,             
        } ,
             {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-07-01",
            'data_final':  "2023-07-31" ,
            "cnpj_fundo": cnpj ,            
        } ,  
        {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-08-01",
            'data_final':  "2023-08-31" ,
            "cnpj_fundo": cnpj ,
        },
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-09-01",
            'data_final':  "2023-09-30" ,
            "cnpj_fundo": cnpj ,             
        } ,    
          {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-10-01",
            'data_final':  "2023-10-31" ,
            "cnpj_fundo": cnpj
                            } ,
            {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-11-01",
            'data_final':  "2023-11-30" ,
            "cnpj_fundo": cnpj , 
        } , {
            'cd_fundo':  cd_fundo ,
            'data_inicial':  "2023-12-01",
            'data_final':  "2023-12-31" ,
            "cnpj_fundo": cnpj ,

        }]

        return extracao


    def extracao_efinanceira(self):
        service_extracao = ExtratorMovimentacoes()
        fundos = ListFundosService(os.environ.get("JCOT_USER") ,
                                     os.environ.get("JCOT_PASSWORD")).listFundoRequest()
        # fundos_dtvm = fundos[fundos['administrador'] ==  '36113876000191']

        
        fundos_dtvm = [
            {"codigo": "1944" , "cnpj":"17455369000191" } , 
            {"codigo": "6021" , "cnpj":"21824924000182" }  , 
             {"codigo": "38281_SEN01" , "cnpj":"28819553000190" } 
        ]


        extracao = [self.get_2023_year(item['codigo'] , item['cnpj']) 
                    for item in fundos_dtvm]
        

        for item in extracao:
            for periodo in item:
                service_extracao.base_movimentacoes(periodo)


    def CriarInvestidores(self):
        '''buscar dados dos investidores'''
        contas = ContaEfin.objects.values('numconta').distinct()
        cotistas = []
        for item in contas:
            consulta = item['numconta'].split("|")[1].strip()
            print (consulta)
            investidor = InvestidorEfin(cpfcnpj = consulta[0:14] )
            investidor.save()

    def AtualizarInvestidores(self):
        service_atualiza_investidores = AtualizacaoInvestidores()
        # service_atualiza_investidores.atualizar_enderecos()
        # service_atualiza_investidores.atualizar_enderecos_busca_o2()        
        # service_atualiza_investidores.atualizar_nomes()

    def rotinas_pre_arquivos(self):
        '''rotina da efinanceira pre_geracao de arquivos'''
        self.extracao_efinanceira()
        self.CriarInvestidores()
        # self.AtualizarInvestidores()


    def gerar_arquivo_efin(self,data , investidor , fundos):
        '''a data precisa ser um objeto datetime'''

        geracao = GeradorEfinanceira(investidor.cpfcnpj , investidor.nome , 
                                investidor.endereco , investidor.pais , 
                                data, fundos)
        
        geracao.gerar_arquivo_efin()


    def MontarArquivos(self):
        fundos = ListFundosService(os.environ.get("JCOT_USER") ,
                                     os.environ.get("JCOT_PASSWORD")).listFundoRequest()
        
        fundos_dtvm = fundos[fundos['administrador'] ==  '36113876000191']
        
        investidores = InvestidorEfin.objects.all()        

        for investidor in investidores:
            print (investidor.cpfcnpj)

            # self.gerar_arquivo_efin(datetime(2023,7,31) , investidor ,  fundos_dtvm)
            # self.gerar_arquivo_efin(datetime(2023,8,31) , investidor ,  fundos_dtvm)
            # self.gerar_arquivo_efin(datetime(2023,9,30) , investidor ,  fundos_dtvm)
            # self.gerar_arquivo_efin(datetime(2023,10,31) , investidor ,  fundos_dtvm)
            # self.gerar_arquivo_efin(datetime(2023,11,30) , investidor ,  fundos_dtvm)
            self.gerar_arquivo_efin(datetime(2023,12,31) , investidor ,  fundos_dtvm)


    def get(self, request):
        #todo incluir depois a possibilidade de receber
        # uma lista de fundos para ser a base da extração

        # self.rotinas_pre_arquivos()

        self.MontarArquivos()


        return JsonResponse({"message":"Extração Iniciada"})