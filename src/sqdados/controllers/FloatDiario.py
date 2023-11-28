from .DiUpdate import DiCetip
from sqlalchemy import create_engine
import pandas as pd
from db_conection import *






class ArquivoFloatDiario():


    def __init__(self):
         pass


    def importar_arquivo_float(excel_file):
        file = pd.read_excel(excel_file)
        file['VALOR'] =  file['VALOR'].apply(float)
        df_final = file[['ATIVO' ,  "DATA" , "VALOR"]]
        df_final.to_sql("FLOAT_ORIGINAL" , con=DASHBOARD_ENGINE.begin() , index=False , if_exists="append")
        dataInicial = df_final['DATA'].values[0] 
        dataFinal  =  df_final['DATA'].values[-1]


        return {
            "dados" : df_final , 
            "data_inicial":  dataInicial , 
            "data_final":  dataFinal
        }


    def ImportarDi(self , excel_file):
        dados_importacao = self.importar_arquivo_float(excel_file)
        buscar_di = DiCetip(dados_importacao['data_inicial'] , dados_importacao['data_final'])
        di  =  buscar_di.Ditodf()
        di.to_sql("float_di" , con=DASHBOARD_ENGINE , if_exists="append" , index=False)
