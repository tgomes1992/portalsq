from JCOTSERVICE import Mancotistav2Service
from JCOTSERVICE import ManClienteService
from xpapp.models import InvestidoresXp


class InvestidoresSinc:
    '''componente que é responsável por validar a
    integracao do cadastro dos investidores'''

    def consulta_clientes(self):
        pass

    def consulta_cotistas(self):
        pass

    def main_sincronizar_clientes(self):
        clientes_a_sincronizar = self.get_investidores_db()
        for cliente in clientes_a_sincronizar:
            consulta_cliente = ManClienteService("roboescritura","Senh@123").request_consultar_cliente(cliente.CD_CLIENTE)
            if consulta_cliente == "EJCOT-0001":
                cadastrar_clientes = ManClienteService("roboescritura", "Senh@123")
                cadastro = cadastrar_clientes.request_cadastrar_clientes(cliente.cliente_dados_cadastro())
                cliente.statusJcot = True
                cliente.save()
            elif consulta_cliente == "EJCOT-0000":
                cliente.statusJcot = True
                cliente.save()

    def main_sincronizar_cotistas(self):
        clientes_a_sincronizar = self.get_cotistas_db()
        for cliente in clientes_a_sincronizar:
            consulta_cotista = Mancotistav2Service("roboescritura","Senh@123").request_consultar_cotista(cliente.CD_CLIENTE)
            print(consulta_cotista)
            if consulta_cotista == "EJCOT-0001":
                cadastro_cotistas = Mancotistav2Service("roboescritura", "Senh@123")
                cadastro = cadastro_cotistas.request_habilitar_pco_xp(cliente.cotista_dados_cadastro())
                print(cadastro)
                cliente.status_cadastro_cotista = True
                cliente.save()
            elif consulta_cotista == "EJCOT-0000":
                cliente.status_cadastro_cotista = True
                cliente.save()

    def get_investidores_db(self):
        investidores = InvestidoresXp.objects.all()
        cds_investidores = [investidor for investidor in investidores if not investidor.statusJcot]
        return cds_investidores

    def get_cotistas_db(self):
        investidores = InvestidoresXp.objects.all()
        cds_investidores = [investidor for investidor in investidores if not investidor.status_cadastro_cotista]
        return cds_investidores


    def sincronizar_investidores_xp(self):
        print ("Clientes Sincronizados")
        self.main_sincronizar_clientes()
        print ("Cotistas Sincronizados")
        self.main_sincronizar_cotistas()
