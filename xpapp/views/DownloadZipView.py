from io import BytesIO 
import io
import zipfile
import pandas as pd
from django.http import HttpResponse
from django.views.generic import View
from JCOTSERVICE import ConsultaMovimentoPeriodoV2Service , RelPosicaoFundoCotistaService , ListFundosService
from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import date ,  datetime
from ..models import FundoXP
import csv
from pymongo import MongoClient

client = MongoClient('mongodb://Thiago.Conceicao:PZV%7BTaKR1j8n@OTAPLICRJ04/')

jcot_posicoes = client['jcot_posicoes']
colection = jcot_posicoes['posicoes']



class DownloadZipView(View):

    def get_fundos_list(self):
        list_fundos_service = ListFundosService("roboescritura" , "Senh@123")
        return list_fundos_service.listFundoRequest()

    def format_thousands_and_decimals(self,  value):
        return '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',').replace(' ', '.')
    
    def format_thousands_and_decimals_float(self,  value):
        value_c = float(value)
        return '{:,.8f}'.format(value_c).replace(',', ' ').replace('.', ',').replace(' ', '.')
        # return value

    def select_fundo_file_name(self , fundo_cnpj):
        fundo = FundoXP.objects.filter(cnpj = fundo_cnpj).first()

        return fundo.filename

    def format_brazilian_cnpj(self, cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj) < 2:
            raise ValueError("Invalid CNPJ: CNPJ must have at least 2 digits.")


        cnpj = cnpj.rjust(14, '0')

        formatted_cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

        return formatted_cnpj


    def extrair_posicoes_jcot(self, data):
        '''o atributo data precisa ser um datetime'''

        # data_datetime = datetime.strptime(data, "%d/%m/%Y")

        service_posicao = RelPosicaoFundoCotistaService("roboescritura" , "Senh@123")
        service_list_fundos = ListFundosService("roboescritura","Senh@123")


        colection.delete_many({})
        # fundos = FundoXP.objects.all() 
        df = service_list_fundos.listFundoRequest()
        df_xp = df[df['administrador'] == '02332886000104']

        JOBS_posicao = [{"codigo": item['codigo'],  "dataPosicao":  data.strftime("%Y-%m-%d")} 
                for item in df_xp.to_dict("records")]
            
        # JOBS_posicao =  [item.gerar_posicao(data) for item in fundos]
        for job in JOBS_posicao:
            dados  = service_posicao.get_posicoes_json(job)
            if len(dados) != 0: 
                colection.insert_many(dados)

    def classificar_tipo_investidor(self, investidor):
        if "XP " in investidor:
            return "PCO"
        else:
            return "IDENTIFICADO"
        


    def classificar_tipo_de_fundo(self,df ,cd_fundo):
        analise = df[df['codigo'] == cd_fundo].to_dict("records")[0]['tipoFundo']
        if "ABER" in analise:
            return "CFA"
        else:
            return "CFF"
        

    def get_cnpj_fundos(self, df , cd_fundo):
        return self.format_brazilian_cnpj(df[df['codigo'] == cd_fundo].to_dict("records")[0]['cnpj'])


    def get_razao_fundos(self, df , cd_fundo):
        return df[df['codigo'] == cd_fundo].to_dict("records")[0]['razaoSocial']


    def gerar_dataframe_posicao(self):
        cabecalho_posicao = ["Mnemônico Investidor","Investidor","CPF/CNPJ Investidor",
                "Data Referência","Papel Cota","CNPJ Fundo","Quantidade Total","Valor Bruto","Cota" ,  'tipo_arquivo']
        dados = colection.find({})
        fundos_list = self.get_fundos_list()
        df = pd.DataFrame.from_dict(dados)
        df['tipo_investidor'] =  df['cd_cotista'].apply(self.classificar_tipo_investidor)
        df['tipo_fundo'] = df['fundo'].apply(lambda x :self.classificar_tipo_de_fundo(fundos_list , x))
        df['tipo_arquivo'] =  pd.concat([df['tipo_fundo'], df['tipo_investidor']], axis=1).apply(lambda x: '_'.join(x), axis=1)
        df_base_extracao = df[['nmCotista' , 'nmCotista' ,  'cpfcnpjCotista' , 'data' , 'fundo' , 'fundo'  ,  'qtCotas'  , 'vlCorrigido'  , 'valor_cota' ,  'tipo_arquivo' ]]
        df_base_extracao.columns = cabecalho_posicao
        df_base_extracao['CPF/CNPJ Investidor'] = df_base_extracao['CPF/CNPJ Investidor'].apply(self.format_brazilian_cnpj)
        df_base_extracao['Quantidade Total'] = df_base_extracao['Quantidade Total'].apply(self.format_thousands_and_decimals_float)
        df_base_extracao['Valor Bruto'] = df_base_extracao['Valor Bruto'].apply(lambda x : x.replace(".",","))
        df_base_extracao['Cota'] = df_base_extracao['Cota'].apply(self.format_thousands_and_decimals_float)
        df_base_extracao['Data Referência'] = df_base_extracao['Data Referência'].apply(lambda x : datetime.strptime(x ,"%Y-%m-%d").strftime("%d/%m/%Y"))
        df_base_extracao['CNPJ Fundo'] =  df_base_extracao['CNPJ Fundo'].apply(lambda x: self.get_cnpj_fundos(fundos_list , x))
        df_base_extracao['Papel Cota'] =  df_base_extracao['Papel Cota'].apply(lambda x: self.get_razao_fundos(fundos_list , x))
        df_arquivo = df_base_extracao[df_base_extracao['tipo_arquivo'] != "CFF_IDENTIFICADO"]
        return df_arquivo

        
    def gerar_csv_movimentacao(self, data ):
        service_movimentos = ConsultaMovimentoPeriodoV2Service("roboescritura" , "Senh@123")
        fundos = FundoXP.objects.all() 
        data = datetime.strptime(data , "%d/%m/%Y")
        JOBS = [item.gerar_movimentos(data) for item in fundos]
        extracao = []
        for item in JOBS:
            for linha in item:
                extracao.append(linha)
        df = service_movimentos.montar_retorno_xp(extracao)
        df["Conta Corrente"] = ""
        df['Ponto Venda'] = ""
        # Write the DataFrame to the response
        formato = ["Numero Operacao","Investidor" , "Conta Corrente" , "Papel Cota","Ponto Venda","Tipo Operacao","Data Operacao","Data Conversao","Data Liquidacao",
    "Data do Fundo na Movimentacao","Valor","Status","Status Conversao",   "CNPJ do fundo" ]
        
        full_df = df[formato]
        full_df['filename'] =  full_df["CNPJ do fundo"].apply(self.select_fundo_file_name)
        full_df["CNPJ do fundo"] = full_df['CNPJ do fundo'].apply(self.format_brazilian_cnpj)  
        full_df['Valor']  = full_df['Valor'].apply(lambda x :  self.format_thousands_and_decimals(float(x)))

        return full_df


    def post(self, request):
        formato = ["Numero Operacao","Investidor" , "Conta Corrente" , "Papel Cota","Ponto Venda","Tipo Operacao","Data Operacao","Data Conversao","Data Liquidacao",
             "Data do Fundo na Movimentacao","Valor","Status","Status Conversao",   "CNPJ do fundo" ]
    
        if request.POST['tipoarquivo'] ==  'movimentacao':
            request_base = str(request.POST['data'])    
            data = datetime.strptime(request_base , "%d/%m/%Y")
            df = self.gerar_csv_movimentacao(request_base)    

            files = df['filename'].drop_duplicates().values

                
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:                             
                    filename = df[df["filename"] == file]
                    df_name = f"{file}_{data.strftime('%Y')}_{data.strftime('%m')}_{data.strftime('%d')}.csv"           
                    zipf.writestr(df_name, filename[formato].to_csv(index=False , sep=";" ,  quoting = csv.QUOTE_NONE , quotechar= ""  ,  escapechar = ";"))

            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=retornoxp.zip'
            return response
        else:
            data = datetime.strptime(request.POST['data'] , "%d/%m/%Y")
            self.extrair_posicoes_jcot(data)
            valores = ['Mnemônico Investidor' , 	'Investidor'	, 'CPF/CNPJ Investidor' , 	'Data Referência' ,  
                   	'Papel Cota' , 	'CNPJ Fundo' , 	'Quantidade Total' , 'Valor Bruto'	 , 'Cota']
            df = self.gerar_dataframe_posicao()
            files = df['tipo_arquivo'].drop_duplicates().values
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:                             
                    filename = df[df["tipo_arquivo"] == file]
                    df_name = f"{file}_{data.strftime('%Y')}_{data.strftime('%m')}_{data.strftime('%d')}.csv"           
                    zipf.writestr(df_name, filename[valores].to_csv(index=False , sep=";" ,  quoting = csv.QUOTE_NONE , quotechar= ""  ,  escapechar = ";"))

            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=retorno_posicao.zip'
            return response
        

