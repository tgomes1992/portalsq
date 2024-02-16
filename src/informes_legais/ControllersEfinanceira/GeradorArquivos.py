from ..models import InvestidorEfin , ContaEfin
import xml.etree.ElementTree as ET
from datetime import datetime




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
        elemento.set("xmlns=" ,"")

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

    def criar_mes_caixa(self):
        mes_caixa = ET.Element('mesCaixa')
        anoMesCaixa = ET.SubElement(mes_caixa , 'anoMesCaixa')
        anoMesCaixa.text = self.data_final.strftime('%Y%m')
        mov_op_financeira = ET.SubElement( mes_caixa, 'movOpFin')
        #todo lógica para inserir as contas em xml no arquivo

        contas  = ""

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
        with open(f"add/{self.filename}", "wb") as f:
            root.write(f, encoding="utf-8", xml_declaration=True, indent=4)






