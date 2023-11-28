import os
from xmlrpc.client import DateTime
import pandas as pd
from datetime import datetime
from io import BytesIO, StringIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import pandas as pd
from email import encoders
from email.mime.base import MIMEBase
import pickle
import os
from datetime import datetime, date
import pandas as pd
from sqlalchemy import create_engine , text
import numpy as np
import warnings

warnings.filterwarnings("ignore")

pd.options.display.float_format = '{:.2f}'.format

folder = "//Scototrj01/h/CUSTODIA/7 Escrituração de Ativos/1 - Controle das Operações/PMT´S/"

'''
    Leitura dos arquivos das pastas de pmts que estão localizadas , no caminho abaixo do drive h

    H:\CUSTODIA\7 Escrituração de Ativos\1 - Controle das Operações\PMT´S

    O script lê as pastas de CRA , CRI E NC  e envia um e-mail conforme parâmetros da função  "def enviar_emails"

'''
engine = create_engine("mysql+pymysql://conciliacao:4/jdv)sg@OTAPLICRJ04/pmt")



def get_all_events():
    today = datetime.now()
    pmts = pd.read_sql("pmts", con=engine.connect())
    pmts['Data de Liquidação'] = pd.to_datetime(pmts['Data de Liquidação'])
    filt = (pmts["Data de Liquidação"].dt.month == today.month) & (pmts["Data de Liquidação"].dt.year == today.year) & (
                pmts["Data de Liquidação"].dt.day >= today.day)
    filtrado = pmts[filt]
    df_final = filtrado[['Data Original', 'Data da Efetivação', 'Data de Liquidação', 'Título']]
    retorno = df_final.sort_values(by=['Data de Liquidação'])
    return retorno.drop_duplicates()


def get_all_events_api(data):
    today = data
    pmts = pd.read_sql("pmts", con=engine.connect())
    pmts['Data de Liquidação'] = pmts['Data de Liquidação'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
    filt = (pmts["Data de Liquidação"].dt.month == today.month) & (pmts["Data de Liquidação"].dt.year == today.year) & (
                pmts["Data de Liquidação"].dt.day >= today.day)
    filtrado = pmts[filt]
    filtrado['Data de Liquidação'] = filtrado['Data de Liquidação'].dt.strftime("%d/%m/%Y")
    df_final = filtrado[['Data Original', 'Data da Efetivação', 'Data de Liquidação', 'Título']]
    retorno = df_final.sort_values(by=['Data de Liquidação'])
    retorno.columns = ['dtOriginal',  "dtEfetivacao",  "dtLiquidacao" , "titulo"]
    return retorno.drop_duplicates().to_dict("records")


def get_all_events_ativo(ativo):
    pmts = pd.read_sql("pmts", con=engine.connect())
    pmts['Data de Liquidação'] = pmts['Data de Liquidação'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
    filtrado = pmts[(pmts['Título'] == ativo) & (pmts['Data de Liquidação'] >= datetime.today())]
    df_final = filtrado[['Data Original', 'Data da Efetivação', 'Data de Liquidação', 'Título']]
    df_final['Data de Liquidação'] = df_final['Data de Liquidação'].dt.strftime("%d/%m/%Y")
    df_final.columns = ['dtOriginal',  "dtEfetivacao",  "dtLiquidacao" , "titulo"]
    return df_final.drop_duplicates().to_dict("records")


def get_all_ifs():
    pmts = pd.read_sql("pmts", con=engine.connect()).drop_duplicates('Título')
    ativos = [item[1]['Título'] for item in pmts.iterrows()]
    return ativos


def get_all_ifs_df():
    pmts = pd.read_sql("pmts", con=engine.connect()).drop_duplicates("Título")
    ativos = [item[1]['Título'] for item in pmts.iterrows()]
    return pmts[['Título']].drop_duplicates()


def check_empty(df):
    if df.empty:
        return "Não há eventos para o periodo"
    else:
        return df.to_html(index=False, float_format='{:.2f}'.format)


def float_as_html():
    styles = """

        <style>

            body {
                background-color : aquablue
            }



        </style>


    """

    html = f'''
    <html>

        {styles}

        <body>
        <p>Segue conforme abaixo as PMT´S para o dia de hoje</p>
        <h1>Eventos</h1>        
        {check_empty(get_all_events())}
        </body>
    </html>    
    '''
    return html


def enviar_emails():
    senha = "tAman1993**"  # senha do e-mail
    email = "thiago.conceicao@oliveiratrust.com.br"  # email usuário
    msg = MIMEMultipart()
    html = MIMEText(float_as_html(), 'html')
    msg.attach(html)
    msg['Subject'] = "EVENTOS_DIARIOS_OUTROS_ATIVOS"
    msg['From'] = "thiago.conceicao@oliveiratrust.com.br"  # remetente do e-mail
    msg['To'] = "thiago.conceicao@oliveiratrust.com.br"  # destinatário
    server = smtplib.SMTP_SSL("smtp.gmail.com", '465')
    server.login(email, senha)
    server.sendmail(
        email,
        "thiago.conceicao@oliveiratrust.com.br",  # destinatário
        msg.as_string(), )
    server.quit()
    print("sent!")


