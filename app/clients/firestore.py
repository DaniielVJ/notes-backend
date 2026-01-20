# Aqui construimos el client u objeto que permitira al app conectarse con firestore.
from google.cloud import firestore
# Uvicorn ejecuta la app desde la carpeta base o raiz del proyecto, entonces python carga a la variable pythonpath
# la ruta de la carpeta base, por ende python busca ahi primero los modulos que importamos y si no lo encuentra lo busca
# en sites-packages.
from app.config import settings

project_id = settings.GCP_PROJECT_ID
firestore_id = settings.FIRESTORE_DB_ID

if not project_id:
    raise ValueError("GCP_PROJECT_ID is not specified")

if not firestore_id:
    raise ValueError("FIRESTORE_DB_ID is not specified")

# Realizamos la conexion a firestore, indicandole cual es el project id y database id del servidor de firestore
client = firestore.Client(project=project_id, database=firestore_id)

# Se hace esto, para que cuando el modulo se cargue una unica vez, solo existira ese objeto y usamos la funcion
# para obtener ese unico objeto durante todo el ciclo de vida de la app.
def get_firestore_client():
    return client



