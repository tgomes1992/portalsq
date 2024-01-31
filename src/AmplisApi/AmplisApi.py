import os
import requests
import pandas as pd

class AmplisApi():

    def __init__(self):
        header = self.request_headers()

    def get_api_token(self):
        with requests.Session() as s:
            login_amplis_url = 'https://apps.totvs.amplis.com.br/security/oauth/token'
            api_login = s.post(login_amplis_url, data={'grant_type': 'client_credentials'}, auth=(os.environ.get("AMPLIS_USER"), os.environ.get("AMPLIS_PASSWORD")))
            obtained_token = api_login.json()['access_token']
            return obtained_token

    def request_headers(self):
        api_call_headers = {'Authorization': 'Bearer ' + self.get_api_token(), 'Content-Type': 'application/json'}
        return api_call_headers

    def get_fundos(self):
        consolidado = []
        header = self.request_headers()
        request_call = "https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/cadastro-fundos?pagina=1"
        teste = requests.get(request_call,headers=header )
        resposta1 = teste.json()
        paginas = int(resposta1['totalPaginas'])
        for n in range(paginas):
            base = f"https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/cadastro-fundos?pagina={n}"
            r = requests.get(base , headers=header )
            for item in r.json()['conteudo']:
                consolidado.append(item)
        df = pd.DataFrame.from_dict(consolidado)
        df.to_excel("cadastros_amplis2.xlsx")

    def get_carteiras(self):
        consolidado = []
        header = self.request_headers()
        request_call = "https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/fundos/carteira-fundos?pagina=1"
        teste = requests.get(request_call,headers=header )
        resposta1 = teste.json()
        paginas = int(resposta1['totalPaginas'])
        for n in range(paginas):
            base = frequest_call = f"https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/fundos/carteira-fundos?pagina={n}"
            r = requests.get(base , headers=header )
            for item in r.json()['conteudo']:
                consolidado.append(item)
        df = pd.DataFrame.from_dict(consolidado)
        return df

    def get_mapa(self,datainicio,datafim,id,tipocota):
        print (datainicio)
        header = self.request_headers()
        base = f"https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/patrimonio/mapa/evolucao/cota/datainicial/{datainicio}/datafinal/{datafim}/idcarteira/{id}/tipoposicao/{tipocota}"
        # base = f"https://oliveiratrust.totvs.amplis.com.br/amplisapi/ws/v1/patrimonio/mapa/evolucao/cota/datainicial/2023-09-13/datafinal/2023-09-14/idcarteira/e4e0826a84c08bdc0184ca3aa8b91c00/tipoposicao/F"
        r = requests.get(base,headers=header)
        d = r.json()
        df = pd.DataFrame.from_dict(d)
        df['carteira'] = df['carteira'].apply(lambda x: x['codigo'])

        return df


