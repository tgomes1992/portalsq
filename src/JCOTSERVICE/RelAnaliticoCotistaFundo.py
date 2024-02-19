from .CotService import COTSERVICE
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
pd.options.display.float_format = '{:,.2f}'.format

class RelAnaliticoCotistaFundo(COTSERVICE):

    url = 'https://oliveiratrust.totvs.amplis.com.br:443/jcotserver/services/RelMovAnaliticoFundoCotistaService'
    def body_buscar_relatorio(self , dados):
        data = f'''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tot="http://totvs.cot.webservices" xmlns:glob="http://totvs.cot.webservices/global">
      <soapenv:Header>
            {self.header_login()}
   </soapenv:Header>
   <soapenv:Body>
      <tot:obterRelMovAnaliticoFundoCotistaRequest>
         <tot:filtro>
            <!--Optional:-->
            <tot:cdFundo>{dados['cd_fundo']}</tot:cdFundo>
            <tot:dtInicial>{dados['data_inicial']}</tot:dtInicial>
            <tot:dtFinal>{dados['data_final']}</tot:dtFinal>
         </tot:filtro>
         <!--Optional:-->
         <glob:messageControl>
            <glob:user>{self.user}</glob:user>
            <glob:properties>
               <!--Zero or more repetitions:-->
               <glob:property name="?" value="?"/>
            </glob:properties>
         </glob:messageControl>
      </tot:obterRelMovAnaliticoFundoCotistaRequest>
   </soapenv:Body>
</soapenv:Envelope>'''
        return data

    def formatar_resposta(self ,  xml_string, dados):
        movimentos = []

        root = ET.fromstring(xml_string)

        try:
            cotistas = root.findall(".//{http://totvs.cot.webservices}cotista")
            cd_fundo = root.find(".//{http://totvs.cot.webservices}cdFundo").text
            total_cotistas = []
            for cotista in cotistas:
                base = {
                    'cd_cotista': cotista.find(".//{http://totvs.cot.webservices}cdCotista").text ,
                    'cpfCnpj': cotista.find(".//{http://totvs.cot.webservices}noCpfCnpj").text ,
                    "aplicacao_principal": cotista.find(".//{http://totvs.cot.webservices}totalAplicacaoCotista").find('.//{http://totvs.cot.webservices}vlOriginal').text ,
                    "aplicao_operacao": cotista.find(".//{http://totvs.cot.webservices}totalAplicacaoCotista").find('.//{http://totvs.cot.webservices}vlOperacao').text ,
                    "resgate_principal": cotista.find(".//{http://totvs.cot.webservices}totalResgatesCotista").find('.//{http://totvs.cot.webservices}vlOriginal').text,
                    "resgate_operacao": cotista.find(".//{http://totvs.cot.webservices}totalResgatesCotista").find('.//{http://totvs.cot.webservices}vlOperacao').text ,
                    "data_final": datetime.strptime(dados['data_final'] ,  "%Y-%m-%d") ,
                    "cd_fundo":  cd_fundo
            }
                total_cotistas.append(base)
            pd.DataFrame.from_dict(total_cotistas).to_excel("relatorio.xlsx")
            return total_cotistas
        except Exception as e:
            print (e)
            pass


    def get_dados_cotistas(self, xml_string):
        movimentos  = []
        pass

    def get_movimento_periodo_request(self , dados):
        base_request = requests.post(self.url, self.body_buscar_relatorio(dados))
        movimentos = self.formatar_resposta(base_request.content.decode('utf-8') , dados )
        return movimentos