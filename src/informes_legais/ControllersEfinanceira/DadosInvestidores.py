import requests
import pandas as pd
from ..models import InvestidorEfin
import os
from JCOTSERVICE import ManEnderecoService , ManClienteService

class AtualizacaoInvestidores():


    service_endereco = ManEnderecoService(os.environ.get("JCOT_USER") ,
                                          os.environ.get("JCOT_PASSWORD"))

    service_cliente = ManClienteService(os.environ.get("JCOT_USER") ,
                                          os.environ.get("JCOT_PASSWORD"))

    def atualizar_enderecos(self):
        investidores = InvestidorEfin.objects.filter(nome="").all()

        #atualização do endereço de cada uma das pessoas
        for investidor in investidores:
            endereco = self.service_endereco.request_consultar_endereco_geral(str(investidor.cpfcnpj))
            try:
                a_atualizar = InvestidorEfin.objects.filter(cpfcnpj=investidor.cpfcnpj).first()
                a_atualizar.endereco = endereco['endereco_efinanceira']
                a_atualizar.pais = endereco['dsPais'][0:2]
                a_atualizar.save()
            except Exception as e:
                print(e)


    def atualizar_nomes(self):
        investidores = InvestidorEfin.objects.filter(nome="").all()

        for investidor in investidores:
            nome = self.service_cliente.request_consultar_cliente_nome(str(investidor.cpfcnpj))
            try:
                a_atualizar = InvestidorEfin.objects.filter(cpfcnpj=investidor.cpfcnpj).first()
                a_atualizar.nome = nome
                a_atualizar.save()
            except Exception as e:
                print(e)

        print ("busca_enderecos_concluida")





