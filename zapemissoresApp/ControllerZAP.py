from .ZAPRequest import ZAP



# ZAP("THIAGO.CONCEICAO","b$54f6Ow\TT")



class ControllerZAP():


    def get_saldos(self,data):
        zap = ZAP("THIAGO.CONCEICAO","b$54f6Ow\TT")
        df = zap.zap_saldo_cc(data.strftime("%d/%m/%Y"))
        return df

    def alerta_diario(self,data):
        df = self.get_saldos(data)        
        return df[df['ValorSaldoTotal'] >= 99999.99][["NomeTitular" ,"ValorSaldoTotal","ValorSaldoBloqueado" , "ValorSaldoDisponivel"]]