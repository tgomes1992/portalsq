from intactus.osapi import o2Api
from sqlalchemy import create_engine , text
from datetime import date , datetime
import pandas as pd


class Ativoso2Sinc():

    engine = create_engine("mysql+pymysql://conciliacao:4/jdv)sg@OTAPLICRJ04/portal_escrituracao")

    api =  o2Api("thiago.conceicao","DBCE0923-9CE3-4597-9E9A-9EAE7479D897")

    def get_cd_jcot( self,base_dict):
        if base_dict['origemCodigoInstrumentoFinanceiro'] == "JCOT":
            return base_dict['descricao']
        else:
            return  False

    def get_cd_jcot_lista(self,lista_base_dict):
        cd_jcot = []
        for item in lista_base_dict:
            teste =  self.get_cd_jcot(item)
            if teste:
                cd_jcot.append(teste)
        try:
            return cd_jcot[0]
        except Exception as e:
            return "Sem Código Jcot"
        
    def get_ativos_extracao(self):       

        ativos = self.api.get_ativos()

        db = self.engine.connect()
        db.execute(text("delete from ativos_o2"))
        db.commit()
  

        ativos.dropna(subset = ['dataFimRelacionamento'], inplace=True)
        ativos['cd_jcot'] =  ativos['codigosInstrumentosFinanceiros'].apply(self.get_cd_jcot_lista)
        ativos['dataFimRelacionamento'] =  ativos['dataFimRelacionamento'].apply(lambda x: datetime.strptime(x[0:10],"%Y-%m-%d"))
        
        nativo = ativos.drop(['codigosInstrumentosFinanceiros'] , axis="columns").to_sql("ativos_o2", con=self.engine , if_exists="append")
        
        return nativo
    
    def get_cds_o2(self):

        ativos_rf = [
            "DEB",
            "CRI",
            "CRA",
            "CDCA",
            "LF",
            "AÇÃO",
            "NC"]

        # self.get_ativos_extracao()

        table = pd.read_sql("ativos_o2" , con=self.engine.connect() )
        ntable = table[~table['nomeTipoInstrumentoFinanceiro'].isin(ativos_rf)]
        return ntable['descricao'].values
            
    def get_ativos_o2_list(self):

        ativos_rf = [
            "DEB",
            "CRI",
            "CRA",
            "CDCA",
            "LF",
            "AÇÃO",
            "NC"]

        # self.get_ativos_extracao()

        table = pd.read_sql("ativos_o2" , con=self.engine.connect() )
        ntable = table[~table['nomeTipoInstrumentoFinanceiro'].isin(ativos_rf)]
        return ntable.to_dict("records")

    def get_ativos_unique(self , ativos_o2):
        df = pd.read_sql("ativos_o2" , con=self.engine.connect() )
        return df[df['descricao'] ==  ativos_o2].to_dict("records")[0]






    
