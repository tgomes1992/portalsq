from sqlalchemy import create_engine
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pymongo import MongoClient
from .ExtratorCotasJcot import ExtratorCotas
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

import warnings

warnings.filterwarnings('ignore')

client = MongoClient("mongodb://localhost:27017")

### dados do banco de dados

db = client['posicoes_o2_5401']
colection = db['posicoes_o2']


class GENERATOR_5401():

    def __init__(self):
        self.elemento_fundos = self.criar_fundos()
        self.tipo_cotas = pd.read_excel('tipo_cotas_xp.xlsx')

        pass

    def tipo_pessoa(self, string_cotista):
        if len(string_cotista) == 14:
            return "2"
        elif len(string_cotista) == 11:
            return "1"
        else:
            return "5"

    def classificacao(self, string_cotistas):
        # valida se é uma clearing para retornar o tipo correto
        if "000191" in string_cotistas[-6]:
            return '3'
        else:
            return '1'

    def criar_corpo_inicial(self):
        documento = ET.Element("documento")
        documento.set("cnpj", "36113886000191")
        documento.set('codigoDocumento', '5401')
        documento.set("tipoRemessa", 'I')
        documento.set("dataBase", '2023-12')
        documento.set('nomeResponsavel', "THIAGO MENEZES")
        documento.set("emailResponsavel", "thiago.menezes@oliveiratrust.com.br")
        documento.set("telefoneResponsavel", "02135140000")
        return documento

    def criar_fundos(self):
        fundos = ET.Element("fundos")
        return fundos

    def formatar_pl_fundos(self, string_pl):
        try:
            decimal = str(string_pl.split(".")[1])

            if len(decimal) != 2:

                return string_pl + '0'
            else:
                return string_pl
        except:
            return str(string_pl)

    def criar_fundo(self, cnpj_fundo, quantidade_cotas, quantidade_cotistas, plFundo):
        fundo = ET.Element("fundo")

        fundo.set("cnpjFundo", str(self.formatar_cpf_cnpj(cnpj_fundo)))

        fundo.set("quantidadeCotas", str(round(quantidade_cotas, 2)))

        fundo.set('quantidadeCotistas', str(quantidade_cotistas))

        fundo.set("plFundo", self.formatar_pl_fundos(plFundo))

        return fundo

    def criar_cotistas(self):
        cotistas = ET.Element('cotistas')
        return cotistas

    def incluir_dados(self, string, to_add):
        return string.rjust(to_add, "0")

    def valida_cpf_cnpj(self, numero):
        # Remove caracteres não numéricos
        numero = ''.join(filter(str.isdigit, str(numero)))

        # Verifica se é CPF (11 dígitos)
        if len(numero) <= 11:
            cpf = [int(digito) for digito in numero.zfill(11)]
            # Calcula o primeiro dígito verificador
            dv1 = sum([(i + 1) * cpf[i] for i in range(9)]) % 11
            dv1 = 0 if dv1 < 2 else 11 - dv1
            # Calcula o segundo dígito verificador
            dv2 = sum([(i + 1) * cpf[i] for i in range(10)]) % 11
            dv2 = 0 if dv2 < 2 else 11 - dv2
            # Retorna True se os dígitos verificadores estão corretos
            # return cpf[9] == dv1 and cpf[10] == dv2
            return "CPF"

        # Verifica se é CNPJ (14 dígitos)
        elif len(numero) <= 14:
            cnpj = [int(digito) for digito in numero.zfill(14)]
            # Calcula o primeiro dígito verificador
            dv1 = (sum([(i % 8 + 2) * cnpj[i] for i in range(12)]) % 11) % 10
            # Calcula o segundo dígito verificador
            dv2 = (sum([(i % 8 + 2) * cnpj[i] for i in range(13)]) % 11) % 10
            # Retorna True se os dígitos verificadores estão corretos
            # return cnpj[12] == dv1 and cnpj[13] == dv2
            return "CNPJ"

        # Se não é CPF nem CNPJ, retorna False
        else:
            return False

    def formatar_cpf_cnpj(self, string_documento):
        if self.valida_cpf_cnpj(str(string_documento)) == 'CPF':
            return str(string_documento).zfill(11)
        elif self.valida_cpf_cnpj(str(string_documento)) == 'CNPJ':
            return str(string_documento).zfill(14)
        else:
            return string_documento

    def criar_cotistas_unico(self, cotista):
        # todo criar função para validar o tipo de cotista e a sua respectiva classificação
        try:
            cotista_elemento = ET.Element("cotista")
            cotista_elemento.set("tipoPessoa", self.tipo_pessoa(str(cotista["cpfcnpjInvestidor"])))
            cotista_elemento.set("identificacao", self.formatar_cpf_cnpj(cotista["cpfcnpjInvestidor"]))

            if cotista['cpfcnpjInvestidor'] == '09358105000191':
                cotista_elemento.set('classificacao', str(3))
            else:
                cotista_elemento.set('classificacao', str(1))

            return cotista_elemento
        except Exception as e:
            print(e)

    def criar_cotas(self, lista_cotas):
        # todo criar função para pegar a lógica das cotas
        cotas = ET.Element('cotas')
        for cota in lista_cotas:
            ncota = ET.SubElement(cotas, 'cota')
            ##todo depara de cada uma das classes do jcot
            try:
                tipo_cotas = self.tipo_cotas[self.tipo_cotas['codigo'] == cota['tipoCota']].to_dict("records")[0][
                    'tipo_cota']
            except Exception as e:
                print(e)
                tipo_cotas = "nan"

            ncota.set("tipoCota", str(tipo_cotas))
            ncota.set("qtdeCotas", str(round(cota['qtdeCotas'], 2)))
            ncota.set("valorCota", str(cota['valorCota']))

        return cotas

    def consulta_cotista(self, cnpj_fundo):
        print(cnpj_fundo)
        data = colection.find({"cnpjFundo": cnpj_fundo})

        df = pd.DataFrame.from_dict(data)

        cotistas_cetip = df[df['depositaria'] == 'CETIP'].groupby(['cpfcnpjInvestidor', 'cnpjFundo'])[
            'quantidadeTotalDepositada'].sum().reset_index()
        cotistas_cetip['depositaria'] = 'CETIP'
        cotistas_bolsa_escritural = df[(df['depositaria'] == 'ESCRITURAL') | (df['depositaria'] == 'BOLSA')].groupby(
            ['cpfcnpjInvestidor', 'cnpjFundo'])['quantidadeTotalDepositada'].sum().reset_index()
        cotistas_bolsa_escritural['depositaria'] = 'ESCRITURAL'
        ndf = pd.concat([cotistas_cetip, cotistas_bolsa_escritural])

        retorno = ndf.drop_duplicates()

        return retorno.to_dict("records")

    def consulta_fundos(self):
        # todo criar lógica para ter uma tabela de cotas  , na hora de realizar a geração do arquivo
        fundos = pd.read_csv("fundos.csv").fundos.values
        mongo_pipe = [
            {
                '$group': {
                    '_id': '$cnpjFundo',
                    'quantidadeTotal': {
                        '$sum': '$quantidadeTotalDepositada'
                    },
                    'pl_fundos': {
                        '$sum': '$pl'
                    },
                    'qtdCotistas': {
                        '$addToSet': '$cpfcnpjInvestidor'
                    }
                }
            }, {
                '$addFields': {
                    'pl': 10
                }
            }, {
                '$project': {
                    'cnpj_fundo': '$_id',
                    'quantidadeCotas': '$quantidadeTotal',
                    'qtdCotistas': {
                        '$size': '$qtdCotistas'
                    },
                    'pl_fundos': '$pl_fundos'
                }
            }
        ]

        consulta_fundos = colection.aggregate(mongo_pipe)
        df = pd.DataFrame.from_dict(consulta_fundos)

        return df[df['cnpj_fundo'].isin(fundos)].to_dict("records")

    def get_cotas(self, cnpj_fundo):
        base_df = colection.find({"cnpjFundo": cnpj_fundo})
        df = pd.DataFrame.from_dict(base_df)
        return df

    def consulta_cotas(self, cotista, cnpj_fundo):
        base_df = colection.find({"cnpjFundo": cnpj_fundo, "cpfcnpjInvestidor": cotista})
        df = pd.DataFrame.from_dict(base_df)
        filtro = (df['depositaria'] == 'ESCRITURAL') | (df['depositaria'] == 'BOLSA')
        ndf = df[filtro].groupby(['cpfcnpjInvestidor', 'cota', 'cd_jcot']).sum()[
            'quantidadeTotalDepositada'].reset_index()
        return ndf.to_dict('records')

    def job_gerar_fundos(self, fundo):
        print(fundo)

        fundos_elemento = self.criar_fundo(fundo['cnpj_fundo'],
                                           fundo['quantidadeCotas'],
                                           fundo['qtdCotistas'],
                                           fundo['pl_fundos'])
        ## incluir cotistas do respectivo fundo

        cotistas_elemento = ET.Element("cotistas")
        cotistas = self.consulta_cotista(fundo['cnpj_fundo'])

        cotistas_cetip = []
        for cotista in cotistas:

            if cotista['depositaria'] == 'ESCRITURAL' or cotista['depositaria'] == "BOLSA":
                elemento_cotista = self.criar_cotistas_unico(cotista)
                ## logica para  a criação de cotas
                cotas = self.consulta_cotas(cotista['cpfcnpjInvestidor'], cotista['cnpjFundo'])

                # print (cotas)
                cotas_formatada = [{"tipoCota": item['cd_jcot'], "valorCota": item['cota'],
                                    "qtdeCotas": item['quantidadeTotalDepositada']} for item in cotas]

                cotas_formatada_xml = self.criar_cotas(cotas_formatada)
                elemento_cotista.append(cotas_formatada_xml)
                cotistas_elemento.append(elemento_cotista)
            elif cotista['depositaria'] == 'CETIP':
                cotistas_cetip.append(cotista)

        # montar cotista cetip
        if len(cotistas_cetip) != 0:
            cetip = self.gerar_cotista_cetip(fundo['cnpj_fundo'])
            cotistas_elemento.append(cetip)
        try:
            fundos_elemento.append(cotistas_elemento)
            self.elemento_fundos.append(fundos_elemento)
        except Exception as e:
            print(e)

    def gerar_cotista_cetip(self, cnpj_fundo):
        '''função que consolidaa depositaria cetip'''
        elemento_cotista = self.criar_cotistas_unico({"cpfcnpjInvestidor": "09358105000191"})
        base_df = colection.find({"cnpj_fundo": cnpj_fundo, "depositaria": "CETIP"})
        df_cetip = pd.DataFrame.from_dict(base_df)
        df_grupo = df_cetip.groupby(['cd_jcot', 'cota'])['quantidadeTotalDepositada'].sum().reset_index()
        cotas_formatada = [{"tipoCota": item['cd_jcot'], "valorCota": item['cota'],
                            "qtdeCotas": item['quantidadeTotalDepositada']} for item in df_grupo.to_dict("records")]
        cotas_formatada_xml = self.criar_cotas(cotas_formatada)
        elemento_cotista.append(cotas_formatada_xml)
        return elemento_cotista

    def gerar_5401_completo_mt(self):
        documento = self.criar_corpo_inicial()
        lista_fundos = self.consulta_fundos()

        data = datetime.today()

        with ThreadPoolExecutor(max_workers=7) as executor:
            executor.map(self.job_gerar_fundos, lista_fundos)

        documento.append(self.elemento_fundos)

        xml_string = minidom.parseString(ET.tostring(documento)).toprettyxml(indent="    ")
        file_name = f"arquivo/5401_{data.strftime('%d_%m_%y_%H%M%S')}.xml"
        with open(f'{file_name}', "w") as file:
            file.write(xml_string)

