from intactus.osapi import o2Api
from sqlalchemy import create_engine , text
from datetime import date , datetime
import pandas as pd
import os


class Ativoso2Sinc():

    conection_string = f"mysql+pymysql://{os.environ.get('API_OTESCRITURACAO_DB_USERNAME')}:{os.environ.get('API_OTESCRITURACAO_DB_PASSWORD')}@{os.environ.get('API_OTESCRITURACAO_DB_HOST')}/{os.environ.get('API_OTESCRITURACAO_DB_DATABASE')}"

    engine = create_engine(conection_string)

    api = o2Api(os.environ.get("INTACTUS_LOGIN"),
                               os.environ.get("INTACTUS_PASSWORD"))

    def get_cd_origem_instrumento_financeiro( self,base_dict , tipo):
        if base_dict['nomeOrigemCodigoInstrumentoFinanceiro'] == tipo:
            return base_dict['descricao']
        else:
            return False
        



    def get_cd_jcot_lista(self,lista_base_dict ,  tipo):
        cd_jcot = []
        for item in lista_base_dict:
            teste = self.get_cd_origem_instrumento_financeiro(item , tipo)
            if teste:
                cd_jcot.append(teste)
        try:
            return cd_jcot[0]
        except Exception as e:
            return "Sem Código"
        

    def get_emissor(self , emissor_dict):
        try:
            return {
                "cnpj": emissor_dict['cnpj'],
                'nome': emissor_dict['nome']
            }
        except Exception as e: 
            return {
                "cnpj": "0000000000" , 
                "nome": "Sem Emissor Associado"
            }
        
    def get_ativos_extracao(self):       

        ativos = self.api.get_ativos()

        db = self.engine.connect()
        db.execute(text('DROP TABLE IF EXISTS ativos_o2'))
        db.commit()

        ativos.to_sql("ativos_o2" ,  con=self.engine , if_exists="append")

        return ativos

    def get_ativos_relatorio(self):

        ativos = self.api.get_ativos()
        return ativos
    
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






    
