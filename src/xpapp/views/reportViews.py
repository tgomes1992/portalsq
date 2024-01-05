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
import os
from ..models import FundoXP
import numpy as np
import pandas as pd

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
    template_name = 'process_jobs.html'

    service_posicao = RelPosicaoFundoCotistaService(os.environ.get("JCOT_USER"), os.environ.get("JCOT_PASSWORD"))
    service_list_fundos = ListFundosService(os.environ.get("JCOT_USER"), os.environ.get("JCOT_PASSWORD"))
    api = o2Api(os.environ.get('INTACTUS_LOGIN'), os.environ.get('INTACTUS_PASSWORD'))

    def submit_task(self, ativos, data):
        self.api.get_posicao_list_mongo(ativos, data.strftime("%Y-%m-%d"), jcot_posicoes)

    def get_posicoes_o2(self , data):
        jcot_posicoes['posicoeso2'].delete_many({})
        fundosXP = FundoXP.objects.all()
        jobs = [{'descricao': fundo.descricao_o2, "data": data.strftime("%Y-%m-%d"),
                 "engine": jcot_posicoes , "cd_jcot": fundo.cd_jcot } for fundo in fundosXP]
        job_split = np.array_split(jobs, 6)
        with ThreadPoolExecutor(max_workers=6) as executor:
            # Use the map function to apply the process_job function to each job in parallel
            for lista in job_split:
                executor.submit(self.api.get_posicao_list_fintools, lista)

    def get_posicoes_jcot(self , data):
        jcot_posicoes['jcot_relatorio'].delete_many({})
        df = self.service_list_fundos.listFundoRequest()
        df_xp = df[df['administrador'] == '02332886000104']

        JOBS_posicao = [{"codigo": item['codigo'],  "dataPosicao":  data.strftime("%Y-%m-%d")}
                for item in df_xp.to_dict("records")]
        # Assuming JOBS_posicao is a list of jobs

        # Process jobs
        with ThreadPoolExecutor() as executor:
            # Use the map function to apply the process_job function to each job in parallel
            executor.map(self.process_job, JOBS_posicao)

    def get(self, request, *args, **kwargs):

        data = datetime(2023,12,29)
        self.get_posicoes_o2(data)
        self.get_posicoes_jcot(data)
        #
        return HttpResponse("Jobs processed successfully.")

    def process_job(self, job):
        dados = self.service_posicao.get_posicoes_json(job)
        if len(dados) != 0:
            jcot_posicoes['jcot_relatorio'].insert_many(dados)  # Replace with your actual model and insert logic


    #todo lógica para a geração do novo arquivo da XP
    def construcao_relatorio_consolidado(self):
        fundos = FundoXP.objects.all()
        for fundo in fundos:
            jcot_posicoes['posicoeso2'].find({})

        pass




