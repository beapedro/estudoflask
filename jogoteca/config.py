
from jogoteca import app
import os 

SECRET_KEY = 'pedrinho'

SQLALCHEMY_DATABASE_URI =  \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha='30122004Po!',
        servidor = 'localhost',
        database = 'jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


PFP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/profilepics'
