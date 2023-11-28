import pandas as pd
from intactus.osapi import o2Api
from JCOTSERVICE import RelPosicaoFundoCotistaService
from datetime import datetime


class BatimentoDiario():


    def get_posicao_o2(self ,  ativo ,  data):
        
        data_ajustada = datetime.strptime(data, "%d/%m/%Y")
        api =  o2Api("thiago.conceicao","DBCE0923-9CE3-4597-9E9A-9EAE7479D897")
        df_posicao_o2 = api.get_posicao(data_ajustada,  ativo)
        qtd_o2 = df_posicao_o2.groupby(["Data"])['QuantidadeTotalDepositada'].sum().reset_index()
        valores_o2 = qtd_o2.to_dict("records")[0]['QuantidadeTotalDepositada']
        return valores_o2
        

    def get_posicao_jcot(self , fundo , data):
        servico_posicao_jcot  = RelPosicaoFundoCotistaService("roboescritura" , "Senh@123")
        posicao_jcot =  servico_posicao_jcot.get_posicao_consolidada({"codigo": fundo  , 
                                                      "dataPosicao": datetime.strptime( data, "%d/%m/%Y").strftime("%Y-%m-%d")})
        df = pd.DataFrame.from_dict(posicao_jcot)
        return df

    def get_dados_amplis(self):
        pass


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

