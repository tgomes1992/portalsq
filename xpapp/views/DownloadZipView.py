import os
import io
import zipfile
import pandas as pd
from django.http import HttpResponse
from django.views.generic import View
from JCOTSERVICE import ConsultaMovimentoPeriodoV2Service
from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import date ,  datetime
from ..models import FundoXP
import csv


class DownloadZipView(View):

    def format_thousands_and_decimals(self,  value):
        return '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',').replace(' ', '.')
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


    def gerar_csv(self, data ):
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
        
        
        request_base = str(request.POST['data'])
     
        data = datetime.strptime(request_base , "%d/%m/%Y")


        df = self.gerar_csv(request_base)

                
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
