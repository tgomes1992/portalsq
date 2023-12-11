import pandas as pd
from ..models import CDOT
from intactus.osapi import o2Api
import os



class RemuneraController:


    def __init__(self):
        pass

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


    def get_cds_ot(self):
        codigos = self.get_codigos_ot_o2().to_dict("records")
        for cd in codigos:
            try:
                if cd['codigoInterno'] != None and "OT-" in cd['codigoInterno']:
                    codigo = CDOT(cd_ot = cd['codigoInterno'] ,  
                                tipo_ativo = cd['nomeTipoInstrumentoFinanceiro'])
                    
                    if not CDOT.objects.filter(cd_ot = cd['codigoInterno']).first():               
                        codigo.save()
            except:
                pass
            finally:
                pass

 
                
              
        pass





