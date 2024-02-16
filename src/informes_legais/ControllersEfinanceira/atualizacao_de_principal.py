from JCOTSERVICE import RelPosicaoCotistaService



class BuscaPrincipalJcot():
    
    service = RelPosicaoCotistaService("roboescritura","Senh@123")
    
    def get_dados_principal_por_cotista(self, dados):
        return self.service.request_jcot(dados)
