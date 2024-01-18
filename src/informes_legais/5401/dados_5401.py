import xml.etree.ElementTree as ET
import pandas as pd
import requests
from io import BytesIO
from .validador_cpf_cnpj import ValidadorCpfCnpj
from xml.dom import minidom
import json
from concurrent.futures import ThreadPoolExecutor


'''módulo que pode ser utilizado para extrair as informações do informe 5401'''


endereco = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"

liquidacao = requests.get(endereco)

df = pd.read_csv(BytesIO(liquidacao.content), delimiter=";", encoding="ANSI")
df['CNPJ_FUNDO'] = df['CNPJ_FUNDO'].apply(lambda x: x.replace(".", "")
                                          .replace("/", "")
                                          .replace("-", ""))


def get_fundos_nome(cnpj):
    try:
        return df[df['CNPJ_FUNDO'] == cnpj].to_dict("records")[0]['DENOM_SOCIAL']
    except:
        return "na"


class XML_5401:

    def __init__(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()

    def get_fundos(self):
        fundos = []
        for item in self.root.iter("fundo"):
            fundo = {
                "cnpjFundo": item.get('cnpjFundo'),
                "quantidadeCotas": item.get("quantidadeCotas"),
                "quantidadeCotistas": item.get("quantidadeCotistas"),
                "plFundo": item.get("plFundo"),
            }
            fundos.append(fundo)
        df = pd.DataFrame.from_dict(fundos)
        df['nome_fundo'] = df['cnpjFundo'].apply(get_fundos_nome)
        return df

    def get_cotistas(self):
        cotistas = []
        for item in self.root.iter("cotista"):
            cotista = {
                "tipoPessoa": item.get("tipoPessoa"),
                "identificacao": item.get("identificacao"),
                "classificacao": item.get("classificacao")
            }
            cotistas.append(cotista)
        df = pd.DataFrame.from_dict(cotistas)
        df['validacao_cpf_cnpj'] = df['identificacao'].apply(ValidadorCpfCnpj().definir_validacao)
        return df.drop_duplicates()

    def get_cotas(self):
        cotas = []
        for item in self.root.iter("fundo"):
            cota_element = item.iter("cota")
            for papel_cota in cota_element:
                cota = {
                    "cnpj_fundo": item.get("cnpjFundo"),
                    'tipoCota': papel_cota.get('tipoCota'),
                    "qtdeCotas": papel_cota.get("qtdeCotas"),
                    "valorCota": papel_cota.get("valorCota"),
                }
                cotas.append(cota)
        df = pd.DataFrame.from_dict(cotas)
        return df.drop_duplicates()

    def change_cotistas_job(self, fundo):
        cnpj_fundos = fundo.attrib.get("cnpjFundo")
        cotistas = fundo.findall(".//cotista")
        for cotista in cotistas:
            if cotista.attrib.get("identificacao") in self.lista_cotistas:
                tp_pessoa = \
                self.df_cotistas[self.df_cotistas['identificacao'] == str(cotista.attrib.get("identificacao"))].to_dict(
                    "records")[0]['tipoPessoa']
                cotista.set("tipoPessoa", str(tp_pessoa))

    def ajustar_qtd_cotista_elemento_fundos(self, file):

        # self.df_cotistas.identificacao = self.df_cotistas.identificacao.apply(str)
        # fundos = self.root.findall(".//fundo")
        # for fundo in fundos:
        #     for item in fundo:
        #         cotistas = item
        #         qtd_cotistas = len(cotistas)
        #     fundo.set('quantidadeCotistas' , str(qtd_cotistas) )

        # with ThreadPoolExecutor() as executor:
        #     executor.map(self.change_cotistas_job , fundos)

        xml_string = minidom.parseString(ET.tostring(self.root)).toprettyxml()
        xml_string = "\n".join(line for line in xml_string.split("\n") if line.strip())

        file_name = f"XML_5401_FORMATADO_{file}.xml"
        with open(f'{file_name}', "w") as file:
            file.write(xml_string)

    def gerar_arquivo_validacao(self):
        with pd.ExcelWriter("validacao_arquivo_14012024.xlsx") as writer:
            self.get_fundos().to_excel(writer, sheet_name="fundos", index=False)
            self.get_cotas().to_excel(writer, sheet_name="cotas", index=False)
            self.get_cotistas().to_excel(writer, sheet_name="cotistas", index=False)




