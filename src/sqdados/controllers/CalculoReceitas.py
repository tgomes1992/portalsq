import pandas as pd 
from datetime import date , datetime





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
        df = pd.read_csv(self.file , delimiter=";")
        df['tipo_parcela'] = df['descricao'].apply(lambda x: "anual" if "anual" in x.lower() else "mensal")
        df.to_excel("dados.xlsx")