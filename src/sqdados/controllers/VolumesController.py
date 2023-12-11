from intactus import o2Api
import os
import pandas as pd
from ..models import ArquivoDconciliacao , SecureFilePus






class  VolumesController():

    def getApiO2(self):
        api = o2Api(os.environ.get("INTACTUS_LOGIN") , 
                    os.environ.get("INTACTUS_PASSWORD"))
        return api
    
    
    def get_codigos_ot_o2(self):
        api = self.getApiO2()
        ativos = api.get_ativos()
        df = pd.DataFrame.from_dict(ativos)
        cds_o2 = df[['codigoInterno' , 'nomeTipoInstrumentoFinanceiro']]      
        return cds_o2.drop_duplicates()

    def get_prices(self ,  ativo):
        try:
            pu = SecureFilePus.objects.filter(ativo = ativo).first()
            return pu.issuePrice
        except Exception as e:
            return 0


    def processar_volumes(self):
        base_df = []
        arquivos_dconciliacao = ArquivoDconciliacao.objects.values()
        for item in arquivos_dconciliacao:
            item["data"] = str(item['data'])[0:10]
            item['price'] = self.get_prices(item['ativo'])
            item['volume'] = item['price'] *  item['quantidade']
            base_df.append(item)

        volumes_df = pd.DataFrame.from_dict(base_df)
        return volumes_df
