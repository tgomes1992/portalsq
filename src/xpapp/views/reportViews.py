from django.shortcuts import render , redirect
from django.http import HttpResponse
from ..models import FundoXP
from datetime import datetime
from django.http import HttpResponse
from concurrent.futures import ThreadPoolExecutor
from django.views import View
from .DownloadZipView import  colection , jcot_posicoes
from intactus import o2Api
from JCOTSERVICE import ConsultaMovimentoPeriodoV2Service , RelPosicaoFundoCotistaService , ListFundosService
from ..xphelper.CpfCnpjFormatter import CpfCnpjFormatter
import os
from ..models import FundoXP
import numpy as np
import pandas as pd
from io import BytesIO


def relatorios_diarios_xp(request):
    return render(request,"xpapp/relatorios_diarios_xp.html" )

def relatorio_movimentacao(request):
    if request.method == 'POST':
        service_movimentos = ConsultaMovimentoPeriodoV2Service('roboescritura', "Senh@123" )
        fundos = FundoXP.objects.all() 
        data = datetime.strptime(request.POST['data'] , "%d/%m/%Y")
        JOBS = [item.gerar_movimentos(data) for item in fundos]
        extracao = []
        for item in JOBS:
            for linha in item:
                extracao.append(linha)
        df = service_movimentos.montar_retorno_xp(extracao)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="OT_ORDENS_ENVIO_RETORNO_{data.strftime("%Y_%m_%d")}.csv"'
        df["Conta Corrente"] = ""
        df['Ponto Venda'] = ""


        # Write the DataFrame to the response
        formato = ["Numero Operacao","Investidor" , "Conta Corrente" , "Papel Cota","Ponto Venda","Tipo Operacao","Data Operacao","Data Conversao","Data Liquidacao",
    "Data do Fundo na Movimentacao","Valor","Status","Status Conversao",   "CNPJ do fundo" ]
            
        df[formato].to_csv(response, index=False , sep=";" )
        return response


class ProcessJobsView(View):


    service_posicao = RelPosicaoFundoCotistaService(os.environ.get("JCOT_USER"), os.environ.get("JCOT_PASSWORD"))
    service_list_fundos = ListFundosService(os.environ.get("JCOT_USER"), os.environ.get("JCOT_PASSWORD"))
    api = o2Api(os.environ.get('INTACTUS_LOGIN'), os.environ.get('INTACTUS_PASSWORD'))

    def submit_task(self, ativos, data):
        self.api.get_posicao_list_mongo(ativos, data.strftime("%Y-%m-%d"), jcot_posicoes)

    def get_posicoes_o2(self , data):
        jcot_posicoes['posicoeso2'].delete_many({})

        fundosXP = FundoXP.objects.all()
        jobs = [{'descricao': fundo.descricao_o2, "data": data.strftime("%Y-%m-%d"),
                 "engine": jcot_posicoes , "cd_jcot": fundo.cd_jcot } for fundo in fundosXP if fundo.descricao_o2 != " "]

        job_split = np.array_split(jobs, 8)

        with ThreadPoolExecutor(max_workers=8) as executor:
            # Use the map function to apply the process_job function to each job in parallel
            for lista in job_split:
                executor.submit(self.api.get_posicao_list_fintools, lista)

    def get_posicoes_jcot(self , data):
        jcot_posicoes['jcot_relatorio'].delete_many({})
        df = self.service_list_fundos.listFundoRequest()
        df_xp = df[df['administrador'] == '02332886000104']

        JOBS_posicao = [{"codigo": item['codigo'],  "dataPosicao":  data.strftime("%Y-%m-%d")}
                for item in df_xp.to_dict("records")]


        # Process jobs
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_job, JOBS_posicao)


    # def post(self):
    #     return HttpResponse("teste")

    def get(self, request, data_ajustada):


        data = datetime.strptime(data_ajustada , "%Y-%m-%d" )
        # data = datetime(2023,12,29)
        self.get_posicoes_o2(data)
        self.get_posicoes_jcot(data)
        
        
        self.construcao_relatorio_consolidado()
        df = self.gerar_relatorio(data)
        output = BytesIO()
        
        chunk_size = 10000
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for i in range(0, len(df), chunk_size):
                df_chunk = df.iloc[i:i + chunk_size]
                df_chunk.to_excel(writer, sheet_name='BASE_INFORMES', startrow=i, index=False, header=(i == 0))
            writer.save()
        
       
        # Set the buffer's cursor position to the beginning
        output.seek(0)
        
        # Create a Django response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=XPADM_{data.strftime("%Y")}{data.strftime("%m")}{data.strftime("%d")}_PASSIVOINFORMES.xlsx'
        response.write(output.getvalue())
        
        return response


    def process_job(self, job):
        dados = self.service_posicao.get_posicoes_json(job)
        print (job)
        if len(dados) != 0:
            jcot_posicoes['jcot_relatorio'].insert_many(dados)  # Replace with your actual model and insert logic

    def formatar_pcos(self ,pco_lista, ativo,  emissor):
        formatado = []
        for pco in pco_lista:
            try:
                BASE = {
                    "depositaria": 'PCO' ,
                    "cpf_cnpj": str(pco['cpfcnpjCotista']).strip() ,
                    "investidor":  pco['nmCotista'].strip(),
                    'cnpj_emissor': str(emissor['cnpj']) ,
                    'nomeEmissor': emissor['nome'] ,
                    "ativo": ativo,
                    "quantidadeTotal": float(pco['qtCotas']),
                    'cd_jcot':  pco['fundo'] ,
                    'perfil_tributario': "NÃO CLASSIFICADO"
                }
                formatado.append(BASE)
            except Exception as e:
                print (e)
            
        return formatado

    def buscar_posicoes_o2(self, descricao):
        posicao_o2 = jcot_posicoes['posicoeso2'].find({"cd_escritural": descricao})
        df = pd.DataFrame.from_dict(posicao_o2)
        return df.to_dict("records")



    def job_consulta_arquivo(self , fundo):
        final_df = []
        print (fundo.cd_jcot)
        print (fundo.descricao_o2)

        posicao_o2 = self.buscar_posicoes_o2(fundo.descricao_o2)


        if len(posicao_o2) != 0 : 
            for linha in posicao_o2:
                if linha['cpfcnpjInvestidor'] == 2332886000104:

                    pco_base = jcot_posicoes['jcot_relatorio'].find({'cpfcnpjCotista': str(linha['cpfcnpjInvestidor']) ,
                                                                    'fundo': linha['cd_jcot']})

                    base_ajustada = self.formatar_pcos(pco_base ,linha['cd_escritural'],
                                                       {"cnpj": linha['cnpj_emissor'] ,
                                                        "nome": linha['nomeEmissor'] })

                    for pco in base_ajustada:
                        final_df.append(pco)

                else:
                    try:
                        nlinha = {
                            "depositaria": linha['depositaria'],
                            "cpf_cnpj": str(linha['cpfcnpjInvestidor']).strip(),
                            "investidor": linha['nomeInvestidor'].strip(),
                            'cnpj_emissor': str(linha['cnpj_emissor']),
                            'nomeEmissor': linha['nomeEmissor'],
                            "ativo": linha['cd_escritural'],
                            "quantidadeTotal": linha['quantidadeTotalDepositada'],
                            'cd_jcot': linha['cd_jcot'],
                            'perfil_tributario': linha['nomePerfilTributarioInvestidor']
                        }
                        final_df.append(nlinha)
                    except Exception as e :
                        print (e)

        else:
            pco_base = jcot_posicoes['jcot_relatorio'].find({'fundo': fundo.cd_jcot})
            base_ajustada = self.formatar_pcos(pco_base ,fundo.descricao_o2, {"cnpj": fundo.cnpj , "nome": fundo.nome })
            for item in base_ajustada:
                final_df.append(item)

        if len(final_df) != 0:
            jcot_posicoes['posicao_consolidada'].insert_many(final_df)


    def construcao_relatorio_consolidado(self):
        jcot_posicoes['posicao_consolidada'].delete_many({})
        fundos = FundoXP.objects.all()

        with ThreadPoolExecutor() as executor:
            executor.map(self.job_consulta_arquivo, fundos)

    def gerar_relatorio(self , data):
        consulta = jcot_posicoes['posicao_consolidada'].find({})
        df = pd.DataFrame.from_dict(consulta)
        df['data'] = data.strftime("%d/%m/%Y")
        df.columns = ['id' , 'Depositária' , "CPF/CNPJ Investidor" ,"Investidor" ,  "CNPJ Emissor" , "Emissor" , "Ativo" ,  "Quantidade total" , "cd_jcot" , "Perfil tributário" , "Data" ]
        ordem_xp = [ "Data" ,  'Depositária' , "CPF/CNPJ Investidor" ,"Investidor" ,  "Perfil tributário" ,   "CNPJ Emissor" , "Emissor" , "Ativo" ,  "Quantidade total" , "cd_jcot" ]
        df["CPF/CNPJ Investidor"] = df["CPF/CNPJ Investidor"].apply(lambda x: CpfCnpjFormatter.formatar(str(x)))
        df["CNPJ Emissor"] = df["CNPJ Emissor"].apply(CpfCnpjFormatter.format_to_cnpj)


        return df[ordem_xp]
