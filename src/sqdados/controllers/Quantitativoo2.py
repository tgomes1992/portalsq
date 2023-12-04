from intactus import o2Api
from datetime import datetime
import pandas as pd
import json
from .db_conection import DASHBOARD_ENGINE 
from sqlalchemy import text
import os



class CalculoQuantitativoO2:


    def __init__(self , data ):
        '''A data precisa ser um objeto datetime '''
        self.o2api = o2Api(os.environ.get('INTACTUS_LOGIN'),os.environ.get('INTACTUS_PASSWORD'))
        self.data = data
        self.ativos_renda_fixa = ['DEB' , 'AÇÃO'  , 'CRA' , 'CRI'  , 'NC'  , 'LF']


    def get_ativos_json(self):
        return self.o2api.get_ativos()


    def ativos_na_data(self):
        ''' data_filter precisa ser um datetime object '''
        df_ativos = pd.DataFrame.from_dict(self.get_ativos_json()) 
        df_ativos =  df_ativos.dropna(subset=['dataFimRelacionamento'])
        df_ativos['dataFimRelacionamento'] = df_ativos['dataFimRelacionamento'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        df_ativos['dataInicioRelacionamento'] =  df_ativos['dataInicioRelacionamento'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        df_ativos['dataImplantacao'] = df_ativos['dataImplantacao'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        return df_ativos
    

    def get_fundos_ativos(self):
        df = self.ativos_na_data()
        fundos = df[~df['nomeTipoInstrumentoFinanceiro'].isin(self.ativos_renda_fixa)]
        fundos[(fundos['dataFimRelacionamento'] >= self.data) & (fundos['dataInicioRelacionamento'] <= self.data)]
        fundos_ativos = fundos[(fundos['dataFimRelacionamento'] >= self.data) & (fundos['dataInicioRelacionamento'] <= self.data)]
        fundos_ativos['periodo'] =  self.data.strftime("%m/%Y")
        result =  fundos_ativos.drop(columns=['emissor' , 'codigosInstrumentosFinanceiros' ])
        result[['cnpjEmissor' , 'nomeEmissor' , "periodo"]].drop_duplicates().to_sql('fundos_ativos', con=DASHBOARD_ENGINE , if_exists="append")
        return fundos_ativos
   
    def gerar_relatorio_fundos_ativos(self):
        sql_statement = '''select periodo , 
                           count(distinct cnpjEmissor) as fundos  from fundos_ativos 
                           group by periodo
        '''
        with DASHBOARD_ENGINE.connect() as connection:
            df = pd.read_sql(sql=text(sql_statement) , con=connection)
            return df

        
    def get_outros_ativos_ativos(self):
        df = self.ativos_na_data()
        ativos_renda_fixa = ['DEB' , 'AÇÃO'  , 'CRA' , 'CRI'  , 'NC'  , 'LF']
        temp_d_datas = df[(df['dataFimRelacionamento'] >= self.data) & (df['dataInicioRelacionamento'] <= self.data)]
        temp_d_datas_renda_fixa = temp_d_datas[temp_d_datas['nomeTipoInstrumentoFinanceiro'].isin(ativos_renda_fixa)]
        temp_d_datas_renda_fixa['periodo'] =  self.data.strftime("%m/%Y")
        result =  temp_d_datas_renda_fixa.drop(columns=['emissor' , 'codigosInstrumentosFinanceiros' ])
        result.to_sql("ativos_geral" , con=DASHBOARD_ENGINE , if_exists='append' , index=False)
        return result


    def gerar_relatorio_fundos_ativos(self):
        sql_statement = '''select ativos_geral.periodo  , ativos_geral.nomeTipoInstrumentoFinanceiro  as tipo_ativo , 
	count(nomeTipoInstrumentoFinanceiro) as qtd_outros_ativos from ativos_geral 
group by  ativos_geral.periodo , ativos_geral.nomeTipoInstrumentoFinanceiro 
        '''
        with DASHBOARD_ENGINE.connect() as connection:
            df = pd.read_sql(sql=text(sql_statement) , con=connection)
            return df
