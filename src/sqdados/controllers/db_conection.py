
import os
from sqlalchemy import create_engine




DASHBOARD_ENGINE = create_engine(f"mysql+pymysql://
                                 {os.environ.get('API_OTESCRITURACAO_DB_USERNAME')}:{os.environ.get('API_OTESCRITURACAO_DB_PASSWORD')}
                                 @{os.environ.get('API_OTESCRITURACAO_DB_HOST')}/
                                 {os.environ.get('API_OTESCRITURACAO_DB_DATABASE')}")
