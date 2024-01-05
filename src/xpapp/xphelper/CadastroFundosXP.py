import os
import pandas as pd
from JCOTSERVICE import ListFundosService
from intactus import o2Api
from ..models import FundoXP



class CadastroFundosXP():

    def get_fundos_xp(self):
        fundos = ListFundosService(os.environ.get('JCOT_USER'),  os.environ.get('JCOT_PASSWORD'))
        df = fundos.listFundoRequest()
        xp = "02332886000104"
        return df[df['administrador']==xp].to_dict('records')

    def definir_tipo(self, string):
        if "ABER" in string:
            return "aberto"
        else:
            return "fechado"

    def atualizar_cadastros(self):
        fundos_cadastrados = FundoXP.objects.all()
        fundos_xp_jcot = self.get_fundos_xp()
        codigos = [item.cd_jcot for item in fundos_cadastrados]
        fundos_a_cadastrar = [item for item in fundos_xp_jcot if item['codigo'] not in codigos]

        for item in fundos_a_cadastrar:
            fundo_a_cadastrar = FundoXP(
                cd_jcot = item['codigo'] ,
                nome = item['razaoSocial'],
                cnpj = item['cnpj'] ,
                tipo_fundo = self.definir_tipo(item['tipoFundo'])
            )
            fundo_a_cadastrar.save()


    def atualizar_dados_o2(self):
        api = o2Api(os.environ.get('INTACTUS_LOGIN') , os.environ.get('INTACTUS_PASSWORD'))
        dados_o2  = api.get_ativos()
        fundos_cadastrados = FundoXP.objects.all()

        for fundo in fundos_cadastrados:
            try:
                fundo.descricao_o2 = dados_o2[dados_o2['cd_jcot'] == fundo.cd_jcot].cd_escritural.values[0]
                fundo.save()
            except:
                fundo.delete()