import requests
import pandas as pd
from ..models import InvestidorEfin
import os
from JCOTSERVICE import ManEnderecoService , ManClienteService
from intactus import o2Api

class AtualizacaoInvestidores():


    service_endereco = ManEnderecoService(os.environ.get("JCOT_USER") ,
                                          os.environ.get("JCOT_PASSWORD"))

    service_cliente = ManClienteService(os.environ.get("JCOT_USER") ,
                                          os.environ.get("JCOT_PASSWORD"))
    
    apio2 = o2Api(os.environ.get("INTACTUS_LOGIN") , os.environ.get("INTACTUS_PASSWORD"))


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


    def atualizar_enderecos_busca_o2(self):
        investidores = InvestidorEfin.objects.all()
        # todo  esperar o cabral retornar o endereço e começar a buscar o endereço pela api.

        for investidor in investidores:
            endereco = self.apio2.get_dados_investidor(str(investidor.cpfcnpj))
            try:
                print (endereco['enderecos'])
                # a_atualizar = InvestidorEfin.objects.filter(cpfcnpj=investidor.cpfcnpj).first()
                # a_atualizar.endereco = endereco['endereco_efinanceira']
                # a_atualizar.pais = endereco['dsPais'][0:2]
                # a_atualizar.save()
            except Exception as e:
                print(e)




    def atualizar_nomes(self):
        investidores = InvestidorEfin.objects.filter(nome="").all()

        for investidor in investidores:
            nome = self.service_cliente.request_consultar_cliente_nome(str(investidor.cpfcnpj))
            print (nome)
            try:
                a_atualizar = InvestidorEfin.objects.filter(cpfcnpj=investidor.cpfcnpj).first()
                a_atualizar.nome = nome
                a_atualizar.save()
            except Exception as e:
                print(e)

        print ("busca_enderecos_concluida")





