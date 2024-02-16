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
        # self.headers = {
        #         'Authorization': f'Bearer {self.get_token()}',
        #         'Content-Type': 'application/json'
        # }

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



    def get_posicao(self, data,  codigoInstrumentoFinanceiro ,  cd_jcot ,   headers ):

        # headers = {
        #         'Authorization': f'Bearer {self.get_token()}' ,
        #         'Content-Type': 'application/json'
        # }
        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/Posicao/obterpordatainvestidorinstrumentofinanceiro?codigoInstrumentoFinanceiro={codigoInstrumentoFinanceiro}&data={data}"

        request = requests.get(url,headers=headers)


        retorno = json.loads(request.content)['dados']


        df = pd.DataFrame.from_dict(retorno)
    

        df['cnpj_emissor'] = df['instrumentoFinanceiro'].apply(lambda x : x['cnpjEmissor'])
        df['nomeEmissor'] = df['instrumentoFinanceiro'].apply(lambda x : x['nomeEmissor'])
        df['cd_escritural'] = codigoInstrumentoFinanceiro
        df['cd_jcot'] = cd_jcot

        return df.to_dict("records")

    def get_posicao_r(self, data, codigoInstrumentoFinanceiro):

        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }

        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/Posicao/obterpordatainvestidorinstrumentofinanceiro?codigoInstrumentoFinanceiro={codigoInstrumentoFinanceiro}&data={data}"

        request = requests.get(url, headers=headers)
        # print (request.content)

        retorno = json.loads(request.content)['dados']

        df = pd.DataFrame.from_dict(retorno)


        df['cd_escritural'] = codigoInstrumentoFinanceiro


        return df



    def get_posicao_mongo(self, codigoInstrumentoFinanceiro , headers ):
        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/Posicao/obterpordatainvestidorinstrumentofinanceiro?codigoInstrumentoFinanceiro={ codigoInstrumentoFinanceiro['DescricaoSelecao'] }&data={codigoInstrumentoFinanceiro['data'] }"

        request = requests.get(url,headers=headers)

        retorno = request.json()['dados']

        if len(retorno) > 0:
            print (len(retorno))
            for item in retorno:
                item['dataconsulta'] = codigoInstrumentoFinanceiro['data']
        return retorno


    def get_posicao_fintools(self, data,  codigoInstrumentoFinanceiro ,  cd_jcot ,   headers ):
        url = f"https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/fintools/investidor/posicao/obterpordatainstrumentofinanceiro?codigoInstrumentoFinanceiro={codigoInstrumentoFinanceiro}&data={data}"
        request =  requests.get(url,headers=headers)
        retorno = json.loads(request.content)['dados']
        posicoes = retorno['posicoes']
        cnpj_emissor = retorno['instrumentoFinanceiro']['cnpjEmissor']
        df = pd.DataFrame.from_dict(posicoes)
        df['investidor'] = df['investidor'].apply(lambda x: str(x['cpfcnpj']))
        df["cnpj_emissor"] = cnpj_emissor
        df['nomeEmissor'] = retorno['instrumentoFinanceiro']['nomeEmissor']
        df['cd_escritural'] = codigoInstrumentoFinanceiro
        df['cd_jcot'] = cd_jcot
        return df

    def get_posicao_list_fintools(self, items):
        headers = {
                'Authorization': f'Bearer {self.get_token()}',
                'Content-Type': 'application/json'
        }
        for item in items:
            try:
                print(item['descricao'])
                df = self.get_posicao(item['data'] , item['descricao'] , item['cd_jcot'] , headers)
                item['engine']['posicoeso2'].insert_many(df)
            except Exception as e:
                print (e)


    def get_posicao_list(self, listaAtivos,data,engine):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        for item in listaAtivos:
            try:
                print (item['DescricaoSelecao'])
                df = self.get_posicao(data,item,headers)
                if not df.empty:
                    df['dataconsulta'] = data
                    df.to_sql("posicoeso2",con=engine, if_exists="append")
            except Exception as e:
                print (e)


    def get_posicao_list_mongo(self, listaAtivos):
        headers = {
                'Authorization': f'Bearer {self.get_token()}',
                'Content-Type': 'application/json'
        }
        for item in listaAtivos:
            try:
                print(item['DescricaoSelecao'])
                df = self.get_posicao_mongo(item, headers)
                item['engine']['posicoeso2'].insert_many(df)
                item['engine']['extracao_ok'].insert_one({"ativo":item["DescricaoSelecao"]})
            except Exception as e:
                item['engine']['extracao_com_erro'].insert_one({"ativo":item['DescricaoSelecao']})
                print(e)

    def get_cd_origem_instrumento_financeiro(self, base_dict, tipo):
        if base_dict['nomeOrigemCodigoInstrumentoFinanceiro'] == tipo:
            return base_dict['descricao']
        else:
            return False

    def get_cd_jcot_lista(self, lista_base_dict, tipo):
        cd_jcot = []
        for item in lista_base_dict:
            teste = self.get_cd_origem_instrumento_financeiro(item, tipo)
            if teste:
                cd_jcot.append(teste)
        try:
            return cd_jcot[0]
        except Exception as e:
            return "Sem Código"

    def get_ids_amplis(self):
        url = "http://processamento-app-jcot:5004/get_cotas"
        dados_amplis = requests.get(url)
        df = pd.DataFrame.from_dict(dados_amplis.json(), dtype=str)
        return df

    def get_id_amplis_df(self,df, cd):
        try:
            resultado = df[df['jcot'] == cd].to_dict("records")[0]['id_amplis']
            print (resultado)
            return resultado
        except Exception as e:
            print (e)
            return ""

    def get_ativos(self):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        url = "https://escriturador.oliveiratrust.com.br/intactus/escriturador/api/instrumentofinanceiro/obtertodos"    


        df_amplis = self.get_ids_amplis()

        request =  requests.get(url,headers=headers)

        retorno = json.loads(request.content)['dados']
        df = pd.DataFrame.from_dict(retorno)
        df['cnpjEmissor'] = df['cnpjEmissor'].apply(str)
        df['cd_jcot'] =  df['codigosInstrumentosFinanceiros'].apply(lambda x : self.get_cd_jcot_lista(x, 'JCOT'))
        df['cd_cetip'] =  df['codigosInstrumentosFinanceiros'].apply(lambda x : self.get_cd_jcot_lista(x, 'CETIP'))
        df['cd_bolsa'] =  df['codigosInstrumentosFinanceiros'].apply(lambda x : self.get_cd_jcot_lista(x, 'BOLSA'))
        df['id_amplis'] = df['cd_jcot'].apply(lambda x: self.get_id_amplis_df(df_amplis, x))
        df['cd_escritural'] =  df['codigosInstrumentosFinanceiros'].apply(lambda x : self.get_cd_jcot_lista(x, 'ESCRITURAL'))
        nativo = df.drop(['codigosInstrumentosFinanceiros', "emissor"], axis="columns")
        return nativo


    def get_dados_investidor(self , investidor):
        headers = {
                'Authorization': f'Bearer {self.get_token()}' ,
                'Content-Type': 'application/json'
        }
        url = "https://escriturador.oliveiratrust.com.br/intactus/icorp/api/pessoa/obterporcpfcnpj"

        data = {
            'cpfCnpj': investidor
        }
        print (data)

        dados = requests.get(url , params=data , headers=headers)
        return dados.json()['dados']

