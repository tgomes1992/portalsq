from django.conf import settings
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalescrituracao.settings')
application = get_wsgi_application()
from xpapp.xphelper import MovimentosSinc
from pymongo import MongoClient
from datetime import datetime , timedelta



client =  MongoClient("mongodb://localhost:27017")


start_date = datetime(2022,8,23)



movimentos_sinc_service = MovimentosSinc()



while start_date <= datetime.today():
    data_string =  start_date.strftime("%Y-%m-%d")
    print(data_string)
    df = movimentos_sinc_service.sincronizar_movimentos("31216568000178" , data_string )
    # print (df)
    try:
        client['importacao_lote']['34661_log'].insert_many(df['log'].to_dict("records"))
        client['importacao_lote']['34661_lancamentos'].insert_many(df['lancamentos'].to_dict("records"))
        start_date = start_date + timedelta(days=1)
    except Exception as e:
        print (e)
        start_date = start_date + timedelta(days=1)
        continue