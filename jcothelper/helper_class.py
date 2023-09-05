from JCOTSERVICE import RelPosicaoFundoCotistaService , ListFundosService
from .models import PosicaoFundoJcot
import requests
import pandas as pd
import json
from MAPS_MODULE.extracoes import MapsCentaurus
from datetime import datetime


class BuscarPosicaoJcot():

    def __init__(self):
        self.user = "roboescritura"
        self.password = "Senh@123"
        self.ListFundosService = ListFundosService(self.user , self.password)
        self.posicaoService = RelPosicaoFundoCotistaService(self.user,  self.password)
        self.MapsCentaurus = MapsCentaurus("marcella.rodrigues" , "!Mdetrano16")

    def get_fundos_processamento_auto(self):
        consulta = requests.get("http://otaplicrj04:5004/get_ativos_cadastrados")
        df = pd.DataFrame.from_dict(consulta.json())
        return df

    def get_maps_depara(self,  codigo_fundo):
        df = self.get_fundos_processamento_auto()
        try:
            return df[df['jcot'] == codigo_fundo].to_dict("records")[0]['centaurus']
        except Exception as e:
            print (e)
            return "n"

    def buscar_fundos(self):
        posicoes_cot = []
        PosicaoFundoJcot.objects.all().delete()
        fundos_processamento = self.get_fundos_processamento_auto().jcot.values
        fundos_status = self.ListFundosService.listFundoRequest()
        filtro = fundos_status[fundos_status['codigo'].isin(fundos_processamento)]
        filtro['maps_centaurus'] = filtro['codigo'].apply(self.get_maps_depara)
        for fundo in filtro.to_dict("records"):
            print (fundo)
            data_posicao_datetime = datetime.strptime(fundo['dataPosicao'] , "%Y-%m-%d")
            resultado = self.posicaoService.get_posicao_fundo(fundo)
            posicao_maps = self.MapsCentaurus.get_posicao_consolidada(fundo['maps_centaurus'], "02/01/2023" )
            print(posicao_maps)
            posicao_fundo = PosicaoFundoJcot(cd_fundo = resultado['fundo'] ,
                                             descricao = fundo['maps_centaurus'] ,
                                            quantidade = resultado['valor'] ,
                                            quantidade_maps = float(posicao_maps['Quantidade'].replace(".","").replace(",",".")) )
            posicao_fundo.save()
            posicoes_cot.append(resultado)
        return pd.DataFrame.from_dict(posicoes_cot)