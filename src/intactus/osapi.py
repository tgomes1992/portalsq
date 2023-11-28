import  requests
import json
import logging
import pandas as pd
import pymongo


class o2Api():


    url = "https://escriturador.oliveiratrust.com.br/intactus/iauth/api/auth/token"

    Base_URL= "escriturador.oliveiratrust.com.br/intactus/escriturador/api"

    def __init__(self ,  client_id , client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _get_token_form(self):
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }


    def get_token(self):
        r = requests.post(self.url , self._get_token_form())
        json_response = json.loads(r.text)
        return json_response['access_token']


    def movimentacao_entrar(self ,  cpfcnpj  , instrumento , data, quantidade,  pu):
        corpo =  {            	
            "cpfcnpjInvestidor": cpfcnpj,
            "codigoInstrumentoFinanceiro": instrumento,
            "data": data,
            "quantidade": quantidade,
            "precoUnitario": pu,
            "depositaria": "ESCRITURAL"
        }
        return corpo
    
    def movimentacao_sair(self ,  cpfcnpj  , instrumento , data, quantidade,  pu):
        corpo =  {            	
            "cpfcnpjInvestidor": cpfcnpj,
            "codigoInstrumentoFinanceiro": instrumento,
            "data": data,
            "quantidade": quantidade,
            "precoUnitario": pu,
            "depositaria": "ESCRITURAL"
        }
        return corpo
    

    def movimentacao_bloquear_body(self , cpfcnpj, instrumento, data, quantidade, pu,motivo ,  depositaria):
        corpo = {
            "cpfcnpjInvestidor": cpfcnpj,
            "codigoInstrumentoFinanceiro": instrumento,
            "data": data,
            "quantidade": quantidade,
            "precoUnitario": pu,
            "motivo": motivo,
            "depositaria": depositaria
        }
        return json.dumps(corpo)

    def movimentacao_desbloquear_body(self, cpfcnpj, instrumento, data, quantidade, pu, depositaria):
        corpo = {
            "cpfcnpjInvestidor": cpfcnpj,
            "codigoInstrumentoFinanceiro": instrumento,
            "data": data,
            "quantidade": quantidade,
            "precoUnitario": pu,
            "depositaria": depositaria
        }
        return json.dumps(corpo)


    def registrar_movimentos(self,lista):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        logging.debug('BLOQUEIOS')

        for item in lista['bloqueios']:
                body = self.movimentacao_bloquear_body(item['CpfCnpj'],item['Ativo'],item['Data'],
                                                       item['Quantidade'],1 , item["Motivo gravame"] ,"ESCRITURAL")
                registro = requests.post("https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/movimentacao/bloquear", data=body,
                                         headers=headers)
                logging.debug(registro.content) # trocar o print pelo log das execucoes
                logging.debug(body)
        logging.debug('DESBLOQUEIOS')
        for item in lista['desbloqueios']:
                body = self.movimentacao_desbloquear_body(item['CpfCnpj'],item['Ativo'],item['Data'],
                                                       item['Quantidade'],1,"ESCRITURAL")
                registro = requests.post("https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/movimentacao/desbloquear", data=body,
                                         headers=headers)
                logging.debug(registro.content)  # trocar o print pelo log das execucoes
                logging.debug(body)
        logging.debug('ENTRADAS')
        for item in lista['entradas']:
                body = self.movimentacao_entrar(item['CpfCnpj'],item['Ativo'],item['Data'],
                                                       item['Quantidade'],1,"ESCRITURAL")
                registro = requests.post("https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/movimentacao/entrar", data=body,
                                         headers=headers)
                logging.debug(registro.content)  # trocar o print pelo log das execucoes
                logging.debug(body)
        logging.debug('SAIDAS')
        for item in lista['saidas']:
                body = self.movimentacao_entrar(item['CpfCnpj'],item['Ativo'],item['Data'],
                                                       item['Quantidade'],1,"ESCRITURAL")
                registro = requests.post("https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/movimentacao/sair", data=body,
                                         headers=headers)
                print (registro.content) # trocar o print pelo log das execucoes
                logging.debug(body)



    def get_posicao(self, data,  codigoInstrumentoFinanceiro ):

        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/Posicao/obterpordatainvestidorinstrumentofinanceiro?codigoInstrumentoFinanceiro={codigoInstrumentoFinanceiro}&data={data}"
        
        request =  requests.get(url,headers=headers)

        retorno = json.loads(request.content)['jsonRetorno']
        df = pd.DataFrame.from_dict(json.loads(retorno))

        return df



    def get_posicao_mongo(self, data,  codigoInstrumentoFinanceiro  ,  header):
        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/Posicao/obterpordatainvestidorinstrumentofinanceiro?codigoInstrumentoFinanceiro={ codigoInstrumentoFinanceiro['DescricaoSelecao'] }&data={data}"
        
        request =  requests.get(url,headers=header)

        retorno = json.loads(json.loads(request.content)['jsonRetorno'])

        if len(retorno) > 0:
            for item in retorno:
                item['dataconsulta'] = data
                item["ativoID"] = codigoInstrumentoFinanceiro['InstrumentoFinanceiroID']

        return retorno


    def get_posicao_list(self, listaAtivos,data,engine):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        for item in listaAtivos:
            try:
                print (item['DescricaoSelecao'])
                df =  self.get_posicao(data,item,headers)
                if not df.empty:
                    df['dataconsulta'] =  data
                    df.to_sql("posicoeso2",con=engine , if_exists="append")
            except Exception as e:
                print (e)


    def get_posicao_list_mongo(self, listaAtivos,data,engine):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        for item in listaAtivos:
            try:
                print (item['DescricaoSelecao'])
                df =  self.get_posicao_mongo(data,item,headers)
                engine['posicoeso2'].insert_many(df)      
                engine['extracao_ok'].insert_one({"ativo":item["DescricaoSelecao"]})                   
            except Exception as e:
                engine['extracao_com_erro'].insert_one({"ativo":item['DescricaoSelecao']})   
                print (e)


    def get_ativos(self):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        url = "https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/instrumentofinanceiro/obtertodos"    


        request =  requests.get(url,headers=headers)

        retorno = json.loads(request.content)['dados']

        df = pd.DataFrame.from_dict(retorno)
        df['cnpjEmissor'] = df['cnpjEmissor'].apply(str)

        return df

