from waitress import serve
from portalescrituracao.wsgi import application
import os





if __name__ == '__main__':
    serve(application, port='5001' , host="0.0.0.0")