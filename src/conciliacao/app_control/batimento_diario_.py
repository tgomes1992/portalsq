import os
import pandas as pd
from intactus.osapi import o2Api
from JCOTSERVICE import RelPosicaoFundoCotistaService
from datetime import datetime
from AmplisApi import *
import threading

class BatimentoDiario():


    def __init__(self):
        self.df_o2 = ""
        self.df_jcot = ""
        self.df_amplis = ""



    def get_posicao_o2(self ,  ativo ,  data):

        try:
        
            data_ajustada = datetime.strptime(data, "%d/%m/%Y")
            api =  o2Api(os.environ.get("INTACTUS_LOGIN"),os.environ.get("INTACTUS_PASSWORD"))
            df_posicao_o2 = api.get_posicao_r(data_ajustada,  ativo  )
            qtd_o2 = df_posicao_o2.groupby(["data"])['quantidadeTotalDepositada'].sum().reset_index()
            valores_o2 = qtd_o2.to_dict("records")[0]['quantidadeTotalDepositada']
            df_posicao_o2.to_excel("1.xlsx")
            return valores_o2
        except Exception as e:
            print (e)

    def get_posicao_jcot(self , fundo , data):
        servico_posicao_jcot  = RelPosicaoFundoCotistaService(os.environ.get("JCOT_USER") , os.environ.get("JCOT_PASSWORD"))
        posicao_jcot =  servico_posicao_jcot.get_posicao_consolidada({"codigo": fundo  , 
                                                      "dataPosicao": datetime.strptime( data, "%d/%m/%Y").strftime("%Y-%m-%d")})
        df = pd.DataFrame.from_dict(posicao_jcot)
        self.df_jcot = df
        df.to_excel("2.xlsx")
        return df


    def batimento_por_fundo(self , fundo , data):
        #
        # df_o2 = self.get_posicao_o2(fundo['cd_escritural'],data)
        # df_jcot = self.get_posicao_jcot(fundo['cd_jcot'] , data)
        # df_amplis = self.get_dados_amplis(fundo['id_amplis'], data)


        #todo consolidar os dados de cada um dos dataframes em uma data só
        #todo criar a possibilidade de extrair e fazer a conciliacao por período


       t1 = threading.Thread(target=self.get_posicao_o2, args=(fundo['cd_escritural'],data))
       t2 =  threading.Thread(target=self.get_posicao_jcot, args =  (fundo['cd_jcot'] , data))
       t3  = threading.Thread(target=self.get_dados_amplis, args = (fundo['id_amplis'], data))

       t1.start()
       t2.start()
       t3.start()

       t1.join()
       t2.join()
       t3.join()




    def concilia_fundos(self , fundo):
        '''função responsável por buscar a conciliação dos fundos em todos os sistemas'''

        self.batimento_por_fundo(fundo ,"10/01/2024")

        #todo cruzar os dados dos fundos para que apenas um dataframe seja gerado

        print (self.df_jcot)




    def get_dados_amplis(self , id_amplis , data):

        api_amplis = AmplisApi()
        data_ajustada = datetime.strptime(data, "%d/%m/%Y")
        df_dados_amplis = api_amplis.get_mapa(data_ajustada.strftime("%Y-%m-%d"), data_ajustada.strftime("%Y-%m-%d") , id_amplis , "F" )
        df_dados_amplis.to_excel("3.xlsx")
        self.df_amplis =  df_dados_amplis


    def consolidar_posicao(self ,  dados ,  data):
        print (dados)
        posicao_o2 = self.get_posicao_o2(dados['descricao'] , data)  
        posicao_jcot = self.get_posicao_jcot(dados['cd_jcot'] ,  data)
        posicao_jcot['qtd_o2'] = posicao_o2
        posicao_jcot['o2 x jcot'] = posicao_jcot['qtCotas'] - posicao_jcot['qtd_o2']   
        posicao_jcot['o2 x jcot'] = posicao_jcot["o2 x jcot"].apply(lambda x : round(x , 2))
        posicao_jcot['data'] = data
        posicao_jcot['ativo'] = dados['descricao']
        base = [
            "data", "ativo", "vlAplicacao", "vlCorrigido", 
            "vlIof", "vlIr", "vlResgate", "vlRendimento", 
            "qtd_o2", "qtCotas", "o2 x jcot"]
        return posicao_jcot[base]

