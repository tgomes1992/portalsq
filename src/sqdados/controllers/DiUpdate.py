import os
from datetime import *
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO ,  StringIO


class DiCetip():

    def __init__(self, data_inicial, data_final):
        self.data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        self.data_final = datetime.strptime(data_final, "%d/%m/%Y")

    def gerar_forms(self, strsql=""):

        req1 = {
            'DT_DIA_DE': self.data_inicial.day,
            'DT_MES_DE': self.data_inicial.month,
            'DT_ANO_DE': self.data_inicial.year,
            'DT_DIA_DE_': self.data_inicial.day,
            'DT_MES_DE_': self.data_inicial.month,
            'DT_ANO_DE_': self.data_inicial.year,
            'DT_DIA_ATE': self.data_final.day,
            'DT_MES_ATE': self.data_final.month,
            'DT_ANO_ATE': self.data_final.year,
            'DT_DIA_ATE_': self.data_final.day,
            'DT_MES_ATE_': self.data_final.month,
            'DT_ANO_ATE_': self.data_final.year,
            'str_TipoDescricao': '5',
            'str_TipoFaixaPrazo': '0',
            'str_NomeArquivo': 'WEB_00_DI_Taxas_Over',
            'str_NomeTabela': 'WEB_DI_Taxas_Over',
            'str_Ativo': 'DI',
            'str_ModeloDados': 'TAX_001di',
            'str_TipoEmissao': '0',
            'str_Descricao': '_Geral',
            'str_Populacao': '_Geral',
            'str_FaixaPrazo': '_Geral',
            'str_NrLeilao': '_Geral',
            'str_ModeloLeilao': '_Geral',
            'str_FaixaPrazoTotalizado': '0',
            'str_Emissao': '_Geral',
            'str_ApresentarTipoOp': '0',
            'int_Idioma': '1',
        }
        form_main = {
            'str_NomeArquivo': 'WEB_00_DI_Taxas_Over',
            'str_NomeTabela': 'WEB_DI_Taxas_Over',
            'str_Ativo': 'DI',
            'str_ModeloDados': 'TAX_001di',
            'str_Descricao': 'TTTTTT',
            'str_NrLeilao': '_Geral',
            'str_ModeloLeilao': '_Geral',
            'str_Descricao_1': '',
            'str_Descricao_2': '',
            'str_Descricao_3': '',
            'chk_Descricao_1': '',
            'chk_Descricao_2': '',
            'chk_Descricao_3': '',
            'bln_MostrarContraparte': False,
            'str_Populacao': '_Geral',
            'str_FaixaPrazo': '_Geral',
            'str_FaixaPrazoTotalizado': '0',
            'str_TipoFaixaPrazo': '0',
            'str_TipoEmissao': '0',
            'str_Emissao': '_Geral',
            'str_TipoMoeda': '',
            'str_Moeda': '',
            'str_TipoDescricao': '5',
            'str_ApresentarTipoOp': '0',
            'dta_DataInicio': '01/01/2021',
            'dta_DataFinal': '01/12/2021',
            'str_SQL': strsql,
            'int_Idioma': 1
        }
        forms = {
            'req1': req1,
            'main_request': form_main
        }
        return forms

    def extrair_di(self):
        url1 = "http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v05_template_informacoes_di.asp?str_Modulo=completo&int_Idioma=1&int_Titulo=6&int_NivelBD=2"
        url2 = 'http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v04_10_02_gerador_sql.asp'
        consulta = "http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v04_10_03_consulta.asp"
        with requests.session() as s:
            r = s.get(url1)
            r = s.post(url2, data=self.gerar_forms()['req1'])
            soup = BeautifulSoup(r.content, 'html.parser')
            str_sql = soup.find('input', {'name': 'str_SQL'})['value']
            r = s.post(consulta, self.gerar_forms(strsql=str_sql)['main_request'])
            resultado_consulta = BeautifulSoup(r.content, 'html.parser')
            links = resultado_consulta.find_all('a')
            for link in links:
                if link.text == "Clique aqui para fazer o download do arquivo .XLS":
                    filename = link['href'].split("/")[-1]
            get_xls = f"http://estatisticas.cetip.com.br/astec/temp/{filename}"
            r = s.get(get_xls)
            df =  pd.read_table(BytesIO(r.content) ,  skiprows=6 , encoding="ANSI" ,  sep="\t")
            print (df.head())
            df.columns = [ 'data' , 'n_operacaoes', 'volume' ,  'selic_f' , 
                           'fator' , 'minima' , 'maxima' ,  'dsv' , 
                            'Pdr',  'selic', ]
            return df[['data' ,  'fator' ,  'selic']]
      


    def retornar_di(self):
        base =  []
        with open("temp.txt") as file:
            for i in file:
                l = i.split("\t")
                if len(l) > 5 and l[0][0] != "D":
                    ndict = {
                        'data': datetime.strptime(l[0],"%d/%m/%Y") ,
                        'fator':  float(l[4].replace(",",".")) ,
                        'selic':  float(l[9].replace("\n","").replace(",",".")) ,
                    }
                    base.append(ndict)
        resultado = pd.DataFrame.from_dict(base)
        return resultado

    def Ditodf(self):
        df = self.extrair_di()
        # df = self.retornar_di()

        # os.remove("temp.txt")
        return df



