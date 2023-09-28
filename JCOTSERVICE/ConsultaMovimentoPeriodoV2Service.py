from .CotService import COTSERVICE
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

class ConsultaMovimentoPeriodoV2Service(COTSERVICE):


    url = "https://oliveiratrust.totvs.amplis.com.br:443/jcotserver/services/ConsultaMovimentoPeriodoV2Service"



    def movimento_body(self , dados ):
      base  = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tot="http://totvs.cot.webservices" xmlns:glob="http://totvs.cot.webservices/global">
   <soapenv:Header>

      {self.header_login()}
   </soapenv:Header>
   <soapenv:Body>
      <tot:consultaMovimentoPeriodoV2Request>
         <!--Optional:-->
         <tot:filtro>
            <tot:cdFundo>{dados['cd_fundo']}</tot:cdFundo>
            <tot:dtInicial>{dados['data']}</tot:dtInicial>
            <tot:dtFinal>{dados['data']}</tot:dtFinal>
            <tot:cdTipoMov>{dados['movimento']}</tot:cdTipoMov>          
            <tot:cdTipoConsulta>E</tot:cdTipoConsulta>
         </tot:filtro>
         <!--Optional:-->
         <glob:messageControl>
            <glob:user>{self.user}</glob:user>

            <!--Optional:-->
            <glob:properties>
               <!--Zero or more repetitions:-->
               <glob:property name="?" value="?"/>
            </glob:properties>
         </glob:messageControl>
      </tot:consultaMovimentoPeriodoV2Request>
   </soapenv:Body>
</soapenv:Envelope>'''
      return base


    def formatar_resposta(self , xml_content):

            movimentos = []

            xml_element = ET.fromstring(xml_content)




            for movimento in xml_element.iter("{http://totvs.cot.webservices}movimento"):
                print (movimento)
                item = {}
                item['nota'] = movimento.find("{http://totvs.cot.webservices}idNota").text
                item['investidor'] =  movimento.find("{http://totvs.cot.webservices}nmCotista").text
                item["fundo"] = movimento.find("{http://totvs.cot.webservices}nmFundo").text
                item['operacao'] = movimento.find("{http://totvs.cot.webservices}dsTipoMov").text
                item['data_operacao'] =  movimento.find("{http://totvs.cot.webservices}dtMov").text
                item['dt_liq_fisica'] =  movimento.find("{http://totvs.cot.webservices}dtLiqFisica").text
                item['dt_liq_financeira'] = movimento.find("{http://totvs.cot.webservices}dtLiqFinanceira").text
                item['valor'] = movimento.find("{http://totvs.cot.webservices}vlBruto").text
                item['status'] = "Batido"
                item['status_conversao'] = "Não Efetivado"
                item['data_fundo_movimentacao'] =  movimento.find("{http://totvs.cot.webservices}dtMov").text
                movimentos.append(item)
               #  item['cnpj_fundo'] =  

            return movimentos
        


    def get_movimento_request(self , dados):
        base_request = requests.post(self.url, self.movimento_body(dados))
        return self.formatar_resposta(base_request.content.decode('utf-8'))


    def montar_retorno_xp(self, lista_de_fundos):
      final_report = []
      for fundo in lista_de_fundos:      
         dados = self.get_movimento_request(fundo)
         for lista in dados:
               final_report.append(lista)
      return pd.DataFrame.from_dict(final_report)
