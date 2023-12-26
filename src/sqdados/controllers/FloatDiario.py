from .DiUpdate import DiCetip
from sqlalchemy import create_engine , text
import pandas as pd
from .db_conection import *
from datetime import datetime
from ..models import *



class ArquivoFloatDiario():


    def __init__(self):
         pass


    def importar_arquivo_float(self,excel_file):
        file = pd.read_excel(excel_file)
        file['VALOR'] =  file['VALOR'].apply(float)
        df_final = file[['ATIVO' ,  "DATA" , "VALOR"]]
        df_final['DATA'] = df_final['DATA'].apply(lambda x : datetime.strptime(str(x)[0:10] , "%Y-%m-%d").strftime("%Y-%m-%d"))
        dataInicial = df_final['DATA'].values[0]
        dataFinal  =  df_final['DATA'].values[-1]

        #importação do arquivo diário do float

        for item in df_final.to_dict("records"):
            float_diario = FloatDiario(ativo = item['ATIVO'] ,
                                       data = datetime.strptime(item['DATA'] ,"%Y-%m-%d" ) ,
                                      valor = item['VALOR'] )
            
            validacao_float = FloatDiario.objects.filter(ativo = float_diario.ativo, 
                                                            data = float_diario.data  , 
                                                            valor = float_diario.valor  ).first()
            
            if validacao_float != float_diario:
                float_diario.save() 

        return {
            "data_inicial":  dataInicial , 
            "data_final":  dataFinal       
        }


    def AtualizacaoFloatDiario(self , excel_file):
        dados_importacao = self.importar_arquivo_float(excel_file)
        buscar_di = DiCetip(datetime.strptime(dados_importacao['data_inicial'] ,  "%Y-%m-%d").strftime("%d/%m/%Y") , datetime.strptime(dados_importacao['data_final'] ,  "%Y-%m-%d").strftime("%d/%m/%Y"))
        di  =  buscar_di.extrair_di()
        # Atualização das DI´S diárias
        for item in di.to_dict("records"):
            att_fator = DiFator(data = datetime.strptime(item['data'] , "%d/%m/%Y") , 
                    fator = round(float(item['fator'].replace(",", ".")), 8 ) , 
                    selic = float(item['selic'].replace(",", "."))
                    )
            att_fator.save()


    def gerar_relatorio_float_mensal(self):
        sql_statement = '''with float_mensal as (
                        select distinct 
                            concat(month( sqdados_floatdiario.data) , "/" , year(sqdados_floatdiario.data)) as periodo
                            , sqdados_floatdiario.data , 
                            sqdados_floatdiario.ativo  , 
                            sqdados_floatdiario.valor , 
                            sqdados_difator.fator  , 
                        (sqdados_floatdiario.valor *  sqdados_difator.fator ) -  sqdados_floatdiario.valor as float_diario
                            from sqdados_floatdiario
                        left join sqdados_difator 
                        on sqdados_floatdiario.`data`  = sqdados_difator.`data` 
                        )
                        select periodo , sum(float_diario) as float_mensal from float_mensal
                        group by periodo'''
        with DASHBOARD_ENGINE.connect() as connection:
            df = pd.read_sql(sql=text(sql_statement), con=connection)
            return df
    
    def gerar_relatorio_float_geral(self):
        sql_statement = '''select distinct 
                concat(month( sqdados_floatdiario.data) , "/" , year(sqdados_floatdiario.data)) as periodo
                , sqdados_floatdiario.data , 
                sqdados_floatdiario.ativo  , 
                sqdados_floatdiario.valor , 
                sqdados_difator.fator  , 
            (sqdados_floatdiario.valor *  sqdados_difator.fator ) -  sqdados_floatdiario.valor as float_diario
                from sqdados_floatdiario
            left join sqdados_difator 
            on sqdados_floatdiario.`data`  = sqdados_difator.`data` 
        '''
        with DASHBOARD_ENGINE.connect() as connection:
            df = pd.read_sql(sql=text(sql_statement) , con=connection)
            return df


        # di.to_sql("float_di" , con=DASHBOARD_ENGINE , if_exists="append" , index=False)

