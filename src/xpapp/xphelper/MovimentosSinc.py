from JCOTSERVICE import MovimentoResumidoService
from xpapp.models import MovimentacoesXP
import pandas as pd
from datetime import datetime

class MovimentosSinc():

    def get_movimento_service(self):
        movimento_service = MovimentoResumidoService("roboescritura", "Senh@123")
        return movimento_service

    def get_movimentacoes_sinc(self ,fundo , data):
        '''buscar as movimentacoes que precisam ser sincronizadas
          IMPORTANTE 

          A SINCRONIZAÇÃO DE MOVIMENTAÇÕES GERA UM TOTAL POR INVESTIDOR A SER SINCADO
        
        '''
        movimentacoes  = MovimentacoesXP.objects.filter(statusJcot=False,
                                                        cd_fundo = fundo,
                                                        data_movimentacao = datetime.strptime( data, "%Y-%m-%d"))


        base_df = [movimento.movimentos_base_df() for movimento in movimentacoes]

        if len(base_df) != 0:
            df_movimentos = pd.DataFrame.from_dict(base_df)
            df_agrupado = df_movimentos.groupby(['cd_investidor','cd_fundo','tipo_movimentacao',
                                                 'data_movimentacao','filename']).sum().reset_index()
            movimentos_a_retornar = []
            for movimento in df_agrupado.to_dict("records"):
                novo_movimento = MovimentacoesXP(data_movimentacao=movimento['data_movimentacao'] ,
                                                 cd_investidor=movimento['cd_investidor'] ,
                                                 cd_fundo= movimento['cd_fundo'] ,
                                                 tipo_movimentacao = movimento['tipo_movimentacao'] ,
                                                 valor = movimento['valor'] ,
                                                 filename=movimento['filename'],
                                                 statusJcot = movimento['statusJcot'])
                movimentos_a_retornar.append(novo_movimento)

            ids_a_alterar = [movimento.id for movimento in movimentacoes]


            return {'movimentacoes': movimentos_a_retornar ,
                    'movimentos_alterar_status': ids_a_alterar}
        else:
            return {'movimentacoes': [],
                    'movimentos_alterar_status': []}

    def sincronizar_movimentos(self , fundo , data):
        '''rotina para sincronizar os lançamentos'''
        a_sincronizar =  self.get_movimentacoes_sinc(fundo , data)
        servico = self.get_movimento_service()
        lancamentos = []
        log = []
        print(len(a_sincronizar['movimentacoes']))
        for movimento in a_sincronizar["movimentacoes"]:
            dados = movimento.registro_lancamento()
            # print (dados)
            lancamentos.append(dados)
            lancamento_movimento = servico.movimentoResumidoRequest(dados)
            log.append(lancamento_movimento)
            # print (lancamento_movimento)  #TODO isso é o que vai ser registrado no mongolog

        for id_a_alterar in a_sincronizar["movimentos_alterar_status"]:
            item = MovimentacoesXP.objects.get(id=id_a_alterar)
            item.statusJcot = True
            item.save()

        return {
            "lancamentos": pd.DataFrame.from_dict(lancamentos),
            "log": pd.DataFrame.from_dict(log)
        }









