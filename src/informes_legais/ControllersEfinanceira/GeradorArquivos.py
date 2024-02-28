from ..models import InvestidorEfin , ContaEfin , ResgatesJcot
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from .atualizacao_de_principal import BuscaPrincipalJcot
import pandas as pd
import os
from django.db.models.functions import ExtractMonth
from django.db.models import Sum , Q


class GeradorEfinanceira():

    '''classe responsável por gerar os arquivos da e-financeira ,
     # gerados com base em extrações anteriores'''

    #todo criar método para fazer o ajuste dos 0´s
    #todo criar possível validação para os encerramentos , 
    # verificar quando não tiver valor ult.dia em no último mês do ano
    #gerar o informe para os que não tiveram movimentação mas têm saldo ,
    #ex. consultar a posição e se o cotista não estiver na base de 31/12 ,
    #gerar o informe da mesma forma que os que não
    # têm conta no mês são gerados

    def __init__(self , cpfCnpj , nome , endereco , pais ,  data_final , df_fundos ):
        self.cpfCnpj = cpfCnpj
        self.nome = nome
        self.endereco = endereco
        self.pais = pais
        '''data final no formato datetime '''
        self.data_final = data_final
        self.filename = f"{self.data_final.strftime('%Y%m')}_{self.cpfCnpj}.xml"
        self.df_fundos = df_fundos


    def criar_elemento_base(self):
        # ET.register_namespace()
        elemento = ET.Element("eFinanceira")

        return elemento

    def evento_mov_op_fin(self):
        elemento  = ET.Element('evtMovOpFin')
        elemento.set('ID' ,"ID500000000000591831")
        elemento.set("xmlns" ,"")

        return elemento

    def criar_ideEvento(self):
        ideEvento = ET.Element('ideEvento')
        indRetificacao = ET.SubElement(ideEvento , 'indRetificacao' )
        tpAmb = ET.SubElement(ideEvento , 'tpAmb' )
        aplicEmi = ET.SubElement(ideEvento , 'aplicEmi' )
        verAplic = ET.SubElement(ideEvento , 'verAplic' )
        aplicEmi.text = "1"
        tpAmb.text = "1"
        indRetificacao.text = "1"
        verAplic.text = "00000000000000000001"
        return ideEvento

    def criar_ide_declarante(self):
        ideDeclarante = ET.Element('ideDeclarante')
        cnpjDeclarante = ET.SubElement(ideDeclarante, 'cnpjDeclarante')
        cnpjDeclarante.text = "36113876000191"

        return  ideDeclarante

    def criar_ide_declarado(self):
        ideDeclarado = ET.Element('ideDeclarado')


        tpNI = ET.SubElement(ideDeclarado ,  'tpNI')

        if (len(self.cpfCnpj) == 11):

            tpNI.text = "1"
        
        else:
            tpNI.text = "2"


        NIDeclarado  = ET.SubElement(ideDeclarado ,  'NIDeclarado')
        NIDeclarado.text = self.cpfCnpj
        NomeDeclarado = ET.SubElement(ideDeclarado , 'NomeDeclarado')
        NomeDeclarado.text = self.nome
        EnderecoLivre = ET.SubElement(ideDeclarado , 'EnderecoLivre')
        EnderecoLivre.text = self.endereco
        paisendereco = ET.SubElement(ideDeclarado , 'PaisEndereco')
        pais = ET.SubElement(paisendereco , 'Pais')
        pais.text = self.pais

        return ideDeclarado

    
    def get_tipo_fundo(self, cd_fundo):
        return self.df_fundos[self.df_fundos['codigo'] == cd_fundo].to_dict('records')[0]['tipoFundo']


    def get_contas_periodos_anteriores(self):
   
        numcontas = []
        contas_xml = []
        
        contas = ContaEfin.objects.filter(numconta__contains =  self.cpfCnpj , 
                                           data_final__lte = self.data_final)        
        for conta in contas:
            if conta.numconta not in numcontas:
                numcontas.append(conta.numconta)

        for numconta in numcontas:

            base_conta = {
            "debitos": 0 , 
            "creditos": 0  , 
            'principal': 0 , 
            "Vlrultdia": 0  , 
            "creditosmsmtitu": 0 , 
            'debitosmsmtitu': 0 
                }
            busca_conta = ContaEfin.objects.filter(numconta__contains =  self.cpfCnpj , data_final__lte = self.data_final)
                        
            for registro in busca_conta:
                base_conta['numconta'] = registro.numconta
                base_conta['fundoCnpj'] = registro.fundoCnpj
                base_conta['tipo_fundo'] =  self.get_tipo_fundo(str(registro.numconta).split("|")[0].strip())
        
            contas_xml.append(base_conta)     

        # incluir lógica para validar todos os valores referentes ao preenchimento do numconta        
        return contas_xml
    
    


    def get_contas(self):
   
        numcontas = []
        contas_xml = []
        
        contas = ContaEfin.objects.filter(numconta__contains =  self.cpfCnpj , 
                                           data_final = self.data_final)        
        for conta in contas:
            if conta.numconta not in numcontas:
                numcontas.append(conta.numconta)

        for numconta in numcontas:
            base_conta = {
            "debitos": 0 , 
            "creditos": 0  , 
            'principal': 0 , 
            "Vlrultdia": 0  , 
            "creditosmsmtitu": 0 , 
            'debitosmsmtitu': 0 
                }
            busca_conta = ContaEfin.objects.filter(numconta__contains =  self.cpfCnpj , 
                                           data_final = self.data_final , numconta=numconta)
                        
            for registro in busca_conta:
                base_conta['debitos'] +=  registro.debitos
                base_conta['creditos'] +=  registro.creditos
                base_conta['principal'] +=  registro.principal
                base_conta['numconta'] = registro.numconta
                base_conta['fundoCnpj'] = registro.fundoCnpj
                base_conta['tipo_fundo'] =  self.get_tipo_fundo(str(registro.numconta).split("|")[0].strip())
      
            contas_xml.append(base_conta)     

        # incluir lógica para validar todos os valores referentes ao preenchimento do numconta        
        return contas_xml
    

    def buscar_valor_debitos(self):
        debito = 0
        resgates = ResgatesJcot.objects.filter(data_liquidacao__month = self.data_final.month ,  cd_cotista__contains=str(self.cpfCnpj) ).exclude(cd_tipo="RI").all()

        for item in resgates:
            debito += item.vl_original

        return str(round(debito , 2))


    def criar_conta_xml(self,conta , pgto_acc):

        self.buscar_valor_debitos()
        conta_xml = ET.Element("Conta")
        infoConta = ET.SubElement(conta_xml ,  "infoConta")
        reportavel = ET.SubElement(infoConta ,  'Reportavel')
        pais_reportavel  = ET.SubElement(reportavel ,  "Pais")
        pais_reportavel.text=  "BR"
        tpConta = ET.SubElement(infoConta ,  'tpConta')
        tpConta.text = "3"
        subtpconta = ET.SubElement(infoConta , 'subTpConta')
        subtpconta.text = "301"
        tpnumconta = ET.SubElement(infoConta ,  'tpNumConta')
        tpnumconta.text = 'OECD605'
        numconta = ET.SubElement(infoConta ,  'numConta')
        numconta.text = conta['numconta'].strip().replace(" " ,  "")
        tpRelacaoDeclarado = ET.SubElement(infoConta ,  'tpRelacaoDeclarado')
        tpRelacaoDeclarado.text = '1'
        fundo = ET.SubElement(infoConta ,  'Fundo')
        cnpj_fundo = ET.SubElement(fundo ,  'CNPJ')
        cnpj_fundo.text = conta['fundoCnpj']
        balanco_conta = ET.SubElement(infoConta , "BalancoConta")
        creditos = ET.SubElement(balanco_conta ,  'totCreditos')
        creditos.text = str(round(conta['creditos'] , 2)).replace(".",",")
        debitos = ET.SubElement(balanco_conta ,  'totDebitos')

        # debitos.text = str(round(conta['principal'],2)).replace(".",",")


        debitos.text = self.buscar_valor_debitos().replace(".",",")

        totCreditosMesmaTitularidade = ET.SubElement(balanco_conta ,  'totCreditosMesmaTitularidade')
        totCreditosMesmaTitularidade.text = "0.00".replace(".",",")
        totDebitosMesmaTitularidade = ET.SubElement(balanco_conta ,  'totDebitosMesmaTitularidade')
        totDebitosMesmaTitularidade.text = "0.00".replace(".",",")



        if self.data_final.strftime("%m") == '12':
            print('extraindo vlr ult')
            vlrUltDia = ET.SubElement(balanco_conta ,  'vlrUltDia')
            dados = {
            'cotista': conta['numconta'].split("|")[1].strip() , 
            'data':  '2023-12-29'
              }            
            cd_fundo = conta['numconta'].split("|")[0].strip()
            d = BuscaPrincipalJcot().get_dados_principal_por_cotista(dados)
            df = pd.DataFrame.from_dict(d)
            print (df)
            try:
                vlr_principal = df[df['cd_fundo'] == cd_fundo].to_dict("records")[0]['vlAplicacao']         
                vlrUltDia.text = str(vlr_principal).replace(".",",")
            except Exception as e :
                vlrUltDia.text = str('0,00')


        # todo criar query para pegar os pagamentos acumulados
        # pgto_acc = self.criar_pagamentos_acumulados(conta['numconta'])
        #pgto acc , agora vêm de outro lugar

        infoConta.append(pgto_acc)

        return conta_xml

    def criar_pagamentos_acumulados(self, numconta):
        pgtos_acc = ET.Element("PgtosAcum")
        tpPgto = ET.SubElement(pgtos_acc ,  "tpPgto")
        tpPgto.text = "FATC503"
        totPgtosAcum = ET.SubElement(pgtos_acc ,  'totPgtosAcum')   

        contas_efin_pgtos_acc = ResgatesJcot.objects.filter(data_liquidacao__lte=self.data_final , cd_cotista__contains=str(self.cpfCnpj))     
        total_debitos = 0
        for conta in contas_efin_pgtos_acc:
            print (conta)
            total_debitos += conta.vl_bruto
        totPgtosAcum.text = str(round(total_debitos,2)).replace(".",",")
        return pgtos_acc
       

    def criar_mes_caixa(self , contas):
        mes_caixa = ET.Element('mesCaixa')
        anoMesCaixa = ET.SubElement(mes_caixa , 'anoMesCaixa')
        anoMesCaixa.text = self.data_final.strftime('%Y%m')
        mov_op_financeira = ET.SubElement( mes_caixa, 'movOpFin')
        #todo lógica para inserir as contas em xml no arquivo

        for conta in contas :
            pgto_acc = self.criar_pagamentos_acumulados(conta['numconta'])
            conta_xml = self.criar_conta_xml(conta , pgto_acc)
            mov_op_financeira.append(conta_xml)

        return mes_caixa
    
    def criar_mes_caixa_periodos_anteriores(self , contas):
        mes_caixa = ET.Element('mesCaixa')
        anoMesCaixa = ET.SubElement(mes_caixa , 'anoMesCaixa')
        anoMesCaixa.text = self.data_final.strftime('%Y%m')
        mov_op_financeira = ET.SubElement( mes_caixa, 'movOpFin')
        #todo lógica para inserir as contas em xml no arquivo

        for conta in contas :
            pgto_acc = self.criar_pagamentos_acumulados(conta['numconta'])
            conta_xml = self.criar_conta_xml(conta , pgto_acc)
            mov_op_financeira.append(conta_xml)

        return mes_caixa


    def validacao_pgtos(self):
        contas_efin_pgtos_acc = ContaEfin.objects.filter(data_final__lte=self.data_final , numconta__contains= self.cpfCnpj)
        pgtos_acc = ET.Element("PgtosAcum")
        tpPgto = ET.SubElement(pgtos_acc ,  "tpPgto")
        tpPgto.text = "FATCA503"
        totPgtosAcum = ET.SubElement(pgtos_acc ,  'totPgtosAcum')   

        total_debitos = 0
        for conta in contas_efin_pgtos_acc:
            total_debitos += conta.debitos
        totPgtosAcum.text = str(round(total_debitos,2)).replace(".",",")
        return pgtos_acc


    def criar_pasta_mes(self):
        base_path = os.path.join("add" , self.data_final.strftime('%Y%m'))
        if not os.path.exists(base_path):
            os.mkdir(base_path)
                              




    def gerar_arquivo_efin(self):

        self.criar_pasta_mes()

        base_path = os.path.join('add',self.data_final.strftime('%Y%m'), self.filename)

        contas  =  self.get_contas()

        arquivo = self.criar_elemento_base()
        evtmoop = self.evento_mov_op_fin()
        ideevento  = self.criar_ideEvento()
        idedeclarante = self.criar_ide_declarante()
        idedeclarado = self.criar_ide_declarado()
        
        # condicionar a geração a existência de contas.
        if len(contas) > 0:
            mescaixa = self.criar_mes_caixa(contas)

            arquivo.append(evtmoop)
            arquivo.append(ideevento)
            arquivo.append(idedeclarante)
            arquivo.append(idedeclarado)
            arquivo.append(mescaixa)

            root = ET.ElementTree(arquivo)

            # Write the XML to a file with indentation and UTF-8 encoding
            with open(base_path, "w" ,  encoding='utf-8') as f:
                f.write(minidom.parseString(ET.tostring(arquivo , encoding='utf-8' , xml_declaration=True)).toprettyxml(indent=" "))
        
        elif len(self.get_contas_periodos_anteriores()) >0 :
            contas = self.get_contas_periodos_anteriores()
            mescaixa = self.criar_mes_caixa_periodos_anteriores(contas)
            arquivo.append(evtmoop)
            arquivo.append(ideevento)
            arquivo.append(idedeclarante)
            arquivo.append(idedeclarado)
            arquivo.append(mescaixa)
            with open(base_path, "w" ,  encoding='utf-8') as f:
                f.write(minidom.parseString(ET.tostring(arquivo , encoding='utf-8' , xml_declaration=True)).toprettyxml(indent=" "))

        






