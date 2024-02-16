from ..models import InvestidorEfin , ContaEfin
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from .atualizacao_de_principal import BuscaPrincipalJcot
import pandas as pd


class GeradorEfinanceira():


    def __init__(self , cpfCnpj , nome , endereco , pais ,  data_final):
        self.cpfCnpj = cpfCnpj
        self.nome = nome
        self.endereco = endereco
        self.pais = pais
        '''data final no formato datetime '''
        self.data_final = data_final
        self.filename = f"{self.data_final.strftime('%Y%m')}_{self.cpfCnpj}.xml"

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
        cnpjDeclarante.text = "02150453000120"

        return  ideDeclarante

    def criar_ide_declarado(self):
        ideDeclarado = ET.Element('ideDeclarado')
        tpNI = ET.SubElement(ideDeclarado ,  'tpNI')
        tpNI.text = "1"

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
            "Vlrultdia": 0  , 
            "creditosmsmtitu": 0 , 
            'debitosmsmtitu': 0 
                }
            busca_conta = ContaEfin.objects.filter(numconta__contains =  self.cpfCnpj , 
                                           data_final = self.data_final , numconta=numconta)
            
            for registro in busca_conta:
                base_conta['debitos'] +=  registro.debitos
                base_conta['creditos'] +=  registro.creditos
                base_conta['numconta'] = registro.numconta
                base_conta['fundoCnpj'] = registro.fundoCnpj
            print (base_conta)
            
            contas_xml.append(base_conta)             
        return contas_xml
    
    
    
    def criar_conta_xml(self,conta):
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
        debitos.text = str(round(conta['debitos'],2)).replace(".",",")
        totCreditosMesmaTitularidade = ET.SubElement(balanco_conta ,  'totCreditosMesmaTitularidade')
        totCreditosMesmaTitularidade.text = "0.00".replace(".",",")
        totDebitosMesmaTitularidade = ET.SubElement(balanco_conta ,  'totDebitosMesmaTitularidade')
        totDebitosMesmaTitularidade.text = "0.00".replace(".",",")


        if self.data_final.month == 12:
            vlrUltDia = ET.SubElement(balanco_conta ,  'vlrUltDia')
            dados = {
            'cotista': conta['numconta'].split("|")[0].strip() , 
            'data':  '2023-12-29'
              }            
            cd_fundo = conta['numconta'].split("|")[1].strip()
            d = BuscaPrincipalJcot().get_dados_principal_por_cotista(dados)
            df = pd.DataFrame.from_dict(d)
            try:
                vlr_principal = df[df['cd_fundo'] == cd_fundo].to_dict("records")[0]['vlAplicacao']         
                vlrUltDia.text = str(vlr_principal)
            except Exception as e :
                vlrUltDia.text = str('0,00')
            

        # todo criar query para pegar os pagamentos acumulados

        pgto_acc = self.criar_pagamentos_acumulados(conta['numconta'])

        infoConta.append(pgto_acc)



        return conta_xml



    def criar_pagamentos_acumulados(self, numconta):
        pgtos_acc = ET.Element("PgtosAcum")
        tpPgto = ET.SubElement(pgtos_acc ,  "tpPgto")
        tpPgto.text = "999"
        totPgtosAcum = ET.SubElement(pgtos_acc ,  'totPgtosAcum')
        

        contas_efin_pgtos_acc = ContaEfin.objects.filter(data_final__lte=self.data_final , numconta=numconta)
        
        total_debitos = 0

        for conta in contas_efin_pgtos_acc:
            total_debitos += conta.debitos

        totPgtosAcum.text = str(round(total_debitos,2)).replace(".",",")

        return pgtos_acc


       

    def criar_mes_caixa(self):
        mes_caixa = ET.Element('mesCaixa')
        anoMesCaixa = ET.SubElement(mes_caixa , 'anoMesCaixa')
        anoMesCaixa.text = self.data_final.strftime('%Y%m')
        mov_op_financeira = ET.SubElement( mes_caixa, 'movOpFin')
        #todo lógica para inserir as contas em xml no arquivo

        contas  =  self.get_contas()

        for conta in contas :
            conta_xml = self.criar_conta_xml(conta)
            # print (conta_xml)
            mov_op_financeira.append(conta_xml)

        return mes_caixa


    def gerar_arquivo_efin(self):
        arquivo = self.criar_elemento_base()

        evtmoop = self.evento_mov_op_fin()
        ideevento  = self.criar_ideEvento()
        idedeclarante = self.criar_ide_declarante()
        idedeclarado = self.criar_ide_declarado()
        mescaixa = self.criar_mes_caixa()

        arquivo.append(evtmoop)
        arquivo.append(ideevento)
        arquivo.append(idedeclarante)
        arquivo.append(idedeclarado)
        arquivo.append(mescaixa)

        root = ET.ElementTree(arquivo)

        # Write the XML to a file with indentation and UTF-8 encoding
        with open(f"add/{self.filename}", "w" ,  encoding='utf-8') as f:

            f.write(minidom.parseString(ET.tostring(arquivo , encoding='utf-8' , xml_declaration=True)).toprettyxml(indent=" "))
            
            # root.write(f, encoding="utf-8", xml_declaration=True)






