from .ZAPRequest import ZAP
from dotenv import load_dotenv
import os
from portalescrituracao.settings import variaveis_sq




# ZAP("THIAGO.CONCEICAO","b$54f6Ow\TT")




class ControllerZAP():


    def get_saldos(self,data):
        load_dotenv("\\Scototrj01\h\CUSTODIA\7 Escrituração de Ativos\7 - Scripts, Macros e Automações\.env")
        zap = ZAP(variaveis_sq[variaveis_sq['variaveis'] == "ZAP_LOGIN"].to_dict("records")[0]['valores'],
                  variaveis_sq[variaveis_sq['variaveis'] == "ZAP_PASSWORD"].to_dict("records")[0]['valores'])
        df = zap.zap_saldo_cc(data.strftime("%d/%m/%Y"))
        return df

    def alerta_diario(self,data):
        df = self.get_saldos(data)        
        return df[df['ValorSaldoTotal'] >= 99999.99][["NomeTitular" ,"ValorSaldoTotal","ValorSaldoBloqueado" , "ValorSaldoDisponivel"]]