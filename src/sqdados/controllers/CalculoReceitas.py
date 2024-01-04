import pandas as pd 
from datetime import date , datetime
from ..models import ReceitaMensal




class CalculoRemunera():


    def __init__(self ,  file):
        self.file = file


    def definir_tipo_de_parcela():
        pass


    def arquivos_cetip():
        pass


    def extrair_resultado():
        pass

    def read_file(self):
        df = pd.read_excel(self.file)
        for remuneracao in df.to_dict('records'):
            receita = ReceitaMensal(
                    cd_ot =  remuneracao['cod_operacao'] , 
                    periodicidade = remuneracao['periodicidade'],
                    valor_remuneracao = remuneracao['valor_base'],
                    emissor = remuneracao['razao_social'],
                    emissor_cnpj = remuneracao['cnpj_sacado'],
                    resumo_contrato = remuneracao['descricao'],
                    data_inicio = remuneracao['data_inicio'], 
                    data_fim = remuneracao['data_fim'],
                    tipo_ativo = remuneracao['tipo_ativo'],
            )
            receita.save()
