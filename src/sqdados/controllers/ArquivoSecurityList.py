import pandas as pd
from ..models import SecureFilePus


class ImportacaoSecureClient():

    def leitura_arquivo(self,path):
        df = pd.read_csv(path ,  sep=";" , encoding="iso-8859-1" ,  encoding_errors="replace")
        df_ajustado = df[['TckrSymb' , 'IsseUnitPric']]
        return df_ajustado
    
    def importar_arquivo(self,arquivo):
        dados  = self.leitura_arquivo(arquivo)
        for item in dados.to_dict("records"):
            nativo = SecureFilePus(ativo=item['TckrSymb'] ,
                                  issuePrice=item['IsseUnitPric'])
            if not SecureFilePus.objects.filter(ativo=nativo.ativo ,
                                                 issuePrice = nativo.issuePrice).first():
                nativo.save()
            
    
    













