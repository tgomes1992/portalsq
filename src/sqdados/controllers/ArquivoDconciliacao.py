import pandas as pd
import os
from datetime import datetime
from io import BytesIO

class LeituraArquivoDconciliacao():


    def transformar_inteiro_decimal( self,  inteiro , decimal):
        try:
            int_num = int(inteiro)
            dec_num = int(decimal)
            return f"{int_num}.{dec_num}"
        except:
            return 0


    def formatar_datas( self, data_str):

        try:
            return datetime.strptime(str(data_str[80:88].strip()) , "%Y%m%d")
        except Exception as e:

            return data_str


    def leitura_arquivo( self, path):
        base_df = []
        # file = BytesIO(path)
        # with open(path , 'rb') as arquivodConciliacao:

        destination = open('temp.txt', 'wb+')
        for chunk in path.chunks():
            destination.write(chunk)
        destination.close()    

        with open('temp.txt' , 'r') as arquivodConciliacao:
            for line in arquivodConciliacao:
                base_dict = {}
                base_dict['data'] = self.formatar_datas(line[80:88].strip())
                base_dict['tipo_ativo'] = line[0:5].strip()
                base_dict['ativo'] = line[46:60].strip()
                base_dict['quantidade'] = self.transformar_inteiro_decimal(line[89:100].strip() ,line[101:108].strip() )
                base_df.append(base_dict)
        os.remove("temp.txt")
        return pd.DataFrame.from_dict(base_df)
                

    def leitura_arquivo_file_folder( self, path):
        base_df = []
        # file = BytesIO(path)
        # with open(path , 'rb') as arquivodConciliacao:

        # destination = open('temp.txt', 'wb+')
        # for chunk in path.chunks():
        #     destination.write(chunk)
        # destination.close()    

        with open(path , 'r') as arquivodConciliacao:
            for line in arquivodConciliacao:
                base_dict = {}
                base_dict['data'] = self.formatar_datas(line[80:88].strip())
                base_dict['tipo_ativo'] = line[0:5].strip()
                base_dict['ativo'] = line[46:60].strip()
                base_dict['quantidade'] = self.transformar_inteiro_decimal(line[89:100].strip() ,line[101:108].strip() )
                base_df.append(base_dict)

        return pd.DataFrame.from_dict(base_df)
                
        
        
