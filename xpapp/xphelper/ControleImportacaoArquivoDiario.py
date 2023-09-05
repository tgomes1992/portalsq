from xpapp.models import *
import pandas as pd
from datetime import datetime



class ControleImportacaoArquivoDiario():


    def __init__(self ,  file , filename):
        self.file = file
        self.filename = filename
        self.dia_arquivo = ""


    def criar_investidor_xp(self, nome_investidor , cpf_cnpj):
        if "PASSIVO" in self.filename:
            investidor = InvestidoresXp(NO_CGC = cpf_cnpj.replace(".","").replace("-","").replace("/",""),
                            CD_CLIENTE =   cpf_cnpj.replace(".","").replace("-","").replace("/",""),
                            NM_CLIENTE =  nome_investidor,
                            IC_FJ_PESSOA =  "J",
                            DATA = datetime.today() ,
                            C_ORDEM  = "S",
                            tipo_cotista =  2,
                            statusJcot = False)
            
            return investidor

        else:

            investidor = InvestidoresXp(NO_CGC =  "02332886000104",
                                        CD_CLIENTE =   nome_investidor.replace(" INVESTIMENTOS" ,  ""),
                                        NM_CLIENTE =  nome_investidor,
                                        IC_FJ_PESSOA =  "J",
                                        DATA = datetime.today() ,
                                        C_ORDEM  = "S",
                                        tipo_cotista =  14,
                                        statusJcot = False)
        return investidor

    def rotina_investidores(self , investidores):
        investidorescadastrados =[ item.CD_CLIENTE for item in  InvestidoresXp.objects.all() ]
        a_cadastrar =  [item for item in investidores if item.CD_CLIENTE not in investidorescadastrados ]
        for item in a_cadastrar:
            item.save()

    def rotina_movimentacoes(self , df , data_arquivo):
        lista_movimentacoes  = []
        arquivos_importados =[movimentacao.filename for movimentacao in MovimentacoesXP.objects.all()]
        for movimento in df:
            if 'PASSIVO'  in self.filename:
                nmovimentacao = MovimentacoesXP(cd_investidor= movimento['CPF_CNPJ'].replace('.', '').replace("-","").replace("/","") ,
                                cd_fundo = movimento['PRODUTO'].replace('.', '').replace("-","").replace("/","") ,
                                valor = movimento['VALOR'] ,
                                filename = self.filename ,
                                tipo_movimentacao = movimento['TIPO_MOV'] ,
                                statusJcot = False ,
                                data_movimentacao = datetime.strptime(data_arquivo , "%Y%m%d"))

            else:
                nmovimentacao = MovimentacoesXP(cd_investidor= movimento['NOME'].replace('XP INVESTIMENTOS ', 'XP ') ,
                                cd_fundo = movimento['PRODUTO'].replace('.', '').replace("-","").replace("/","") ,
                                valor = movimento['VALOR'] ,
                                filename = self.filename ,
                                tipo_movimentacao = movimento['TIPO_MOV'] ,
                                statusJcot = False ,
                                data_movimentacao = datetime.strptime(data_arquivo , "%Y%m%d"))

            if nmovimentacao.filename not in arquivos_importados:
                nmovimentacao.save()


    def definir_dia_arquivo(self,  filename):
        if "PASSIVO" in str(filename):
            dia_arquivo =  str(filename).replace("_","").replace(".txt","").split("PASSIVO")[1]
            return dia_arquivo[0:-1]

        else:
            return filename.split("_")[4]
       


    def rotina_criar_arquivo_diario(self , file_name):
        dia_arquivo = self.definir_dia_arquivo(file_name)
        self.dia_arquivo = dia_arquivo
        arquivos_importados = ArquivosXp.objects.all()
        arquivo = ArquivosXp(filename = file_name , filedate = dia_arquivo )
        nomes = [arquivo.filename for arquivo in arquivos_importados]
        if arquivo.filename not in nomes:
            arquivo.save()
            return True
        else:
            return False


    def get_file_data(self):
        print ("Importação iniciada")
        df = pd.read_csv(self.file ,  delimiter=";" ,  decimal=",")

        #ajuste das colunas por conta do arquivo do xpce
        if 'PASSIVO' in self.filename:
            df.columns = ["ID", "NOME","PRODUTO","TIPO_MOV",
                    "COTAS","VALOR","NUM_NOTA",
                    "FORMA","NUMERO_BANCO",
                    "NUMERO_AGENCIA",
                    "NUMERO_CONTA","DIGITO_VERIFICADOR","TIPO_CONTA","ORDEM_ADM",
                    "PGTO_PENALTYFEE","DIAS_PENALTYFEE","PRODUTO_DESTINO",
                    "ORDEM_ORIGEM","NUM_ORDEM","USAR_LIMITES_DIFERENCIADOS",
                    "CPF_CNPJ","RESULTADO" , "CODIGO"]

        df['VALOR'] = df['VALOR'].fillna(0)

        if  self.rotina_criar_arquivo_diario(self.filename):
            print (f"{self.filename} - arquivo importado")            
            investidores = [self.criar_investidor_xp(nome['NOME'] , nome['CPF_CNPJ']) for nome in df.to_dict("records")]
            self.rotina_investidores(investidores) #executa  o processo referente aos investidores
            movimentos =  df.to_dict("records")
            self.rotina_movimentacoes(movimentos , self.dia_arquivo)

    def include_df(self):
        df = pd.read_csv(self.file ,  delimiter=";" ,  decimal=",")
        if 'PASSIVO' in self.filename:
            df.columns = ["ID", "NOME","PRODUTO","TIPO_MOV",
                    "COTAS","VALOR","NUM_NOTA",
                    "FORMA","NUMERO_BANCO",
                    "NUMERO_AGENCIA",
                    "NUMERO_CONTA","DIGITO_VERIFICADOR","TIPO_CONTA","ORDEM_ADM",
                    "PGTO_PENALTYFEE","DIAS_PENALTYFEE","PRODUTO_DESTINO",
                    "ORDEM_ORIGEM","NUM_ORDEM","USAR_LIMITES_DIFERENCIADOS",
                    "CPF_CNPJ","RESULTADO" , "CODIGO"]

        df['VALOR'] = df['VALOR'].fillna(0)

        








