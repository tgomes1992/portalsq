from intactus import o2Api
from datetime import datetime
import pandas as pd
import json
from .db_conection import DASHBOARD_ENGINE
import os



class CalculoQuantitativoO2:


    def __init__(self , data ):
        '''A data precisa ser um objeto datetime '''
        self.o2api = o2Api(os.environ.get('INTACTUS_LOGIN'),os.environ.get('INTACTUS_PASSWORD'))
        # self.data = datetime(2023 , 10 , 31)
        self.data = data


    def get_ativos_json(self):
        return self.o2api.get_ativos()


    def ativos_na_data(self):
        ''' data_filter precisa ser um datetime object '''

        df_ativos = pd.DataFrame.from_dict(json.loads(self.get_ativos_json())) 
        df_ativos =  df_ativos.dropna(subset=['dataFimRelacionamento'])
        df_ativos['dataFimRelacionamento'] = df_ativos['dataFimRelacionamento'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        df_ativos['dataInicioRelacionamento'] =  df_ativos['dataInicioRelacionamento'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        df_ativos['dataImplantacao'] = df_ativos['dataImplantacao'].apply(lambda x : datetime.strptime(x[0:10] , "%Y-%m-%d"))
        # df_ativos.to_excel("ativo.xlsx" , index=False)
        return df_ativos
    

    def get_fundos_ativos(self):
        fundos = self.ativos_na_data()
        fundos[(fundos['dataFimRelacionamento'] >= self.data) & (fundos['dataInicioRelacionamento'] <= self.data)]
        fundos_ativos = fundos[(fundos['dataFimRelacionamento'] >= self.data) & (fundos['dataInicioRelacionamento'] <= self.data)]
        fundos_ativos['periodo'] =  self.data.strftime("%m/%Y")
        return fundos_ativos
   

    def def_outros_ativos_ativos(self):
        df = self.ativos_na_data()
        ativos_renda_fixa = ['DEB' , 'AÇÃO'  , 'CRA' , 'CRI'  , 'NC'  , 'LF']
        temp_d_datas = df[(df['dataFimRelacionamento'] >= self.data) & (df['dataInicioRelacionamento'] <= self.data)]
        temp_d_datas_renda_fixa = temp_d_datas[temp_d_datas['nomeTipoInstrumentoFinanceiro'].isin(ativos_renda_fixa)]
        temp_d_datas_renda_fixa['periodo'] =  self.data.strftime("%m/%Y")
        temp_d_datas_renda_fixa.to_sql("ativos_geral" , con=DASHBOARD_ENGINE , if_exists='append' , index=False)
        temp_d_datas_renda_fixa.to_excel(f"ativos_mensal/{self.data.strftime('%m%Y')}rf.xlsx")
        base = temp_d_datas_renda_fixa.groupby(["nomeTipoInstrumentoFinanceiro"]).count()['id'].reset_index()
        base['periodo'] =  self.data
        base.columns = ['periodo' , 'ativo' , 'total_ativo']
        base.to_excel(f"{self.data.strftime('%m%Y')}.xlsx")
        base.to_sql("ativos_renda_fixa" , con=DASHBOARD_ENGINE , if_exists='append' , index=False)
        temp_d_datas_renda_fixa.to_excel(f"{self.data.strftime('%Y-%m-%d')}.xlsx" ,  index=False)
        return temp_d_datas_renda_fixa





        



