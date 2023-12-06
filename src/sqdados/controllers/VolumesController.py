from intactus import o2Api
import os
import pandas as pd







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


