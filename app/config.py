import os
from pathlib import Path
from dotenv import load_dotenv

# Obtenemos la ruta raiz o base del proyecto, es la carpeta donde se encuentran todos los archivos dentro
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargamos las variables de entorno del archivo del cual le pasamos el path o ruta.
# os.path.join, permite crear una ruta compatible con el S.O donde se este ejecutando el programa.
# load_dotenv(os.path.join(BASE_DIR, '.env.local')) # DESCOMENTAR EN LOCAL O DESARROLLO


# clase para abstraer o representar las configuraciones
class Settings:
    # Cualquier valor de una variable de entorno se carga como un string, aunque esta contenga como valor o el formato de una lista, diccionario.
    GCP_PROJECT_ID: str = os.getenv('GCP_PROJECT_ID')    
    FIRESTORE_DB_ID: str = os.getenv('FIRESTORE_DB_ID')


# Creamos una instancia u objeto que cuando requeramos acceder al valor de una configuracion en cualquier
# parte del programa, utilizaremos este objeto.
settings = Settings()



