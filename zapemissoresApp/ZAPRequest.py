import requests 
import pandas as pd
from io import BytesIO



class ZAP():

    def __init__(self,user , password):
        self.user =  user
        self.password  =  password
        
    
    def zap_login(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
        with requests.session() as s:
            log_page = 'https://zap-cfi:3000/logar'
            json_log = {"url": "logar", "method": "post", "internal": "true",
                        "data": {"conexao": 0, "dadosLogin": {"Senha": self.password, "Usuario": self.user}}}
            r = s.post(log_page, json=json_log, headers=headers, verify=False)

            return s


    def zap_saldo_cc(self , dia):
        with self.zap_login() as s:
                r =  s.get("https://zap-cfi:3000/0/e/1/relatorios-ccb/saldoContasCorrentes" , verify=False)
                zapcc = {"url":"relatorios-ccr/saldoContasCorrentes?TamanhoPagina=700&Pagina=1","method":"post","modulo":"CCR","data":{"ClassificacaoConta": ["2"] ,  "Data":dia}}
                r = s.post("https://zap-cfi:3000/service" , json=zapcc , verify=False)
                resposta = r.json()['Contexto']['Dados']
                df = pd.DataFrame.from_dict(resposta)
                return df


