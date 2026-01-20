from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# La aplicacion completa o API es una instancia u objeto de la clase FastAPI
# que internamente implementa el estandar wsgi y asgi para ser ejecutada por los servidores web.

app = FastAPI()


# Cors, es para indicarle al navegador que nos envia un request desde un origen, si ese origen tiene permitido
# revisar la informacion de el response que le enviamos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Cambiar a la url o origen de nuestro frontend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) # Metodo para añadir middlewares a la app



# Endpoint basico "Hello world"
# El decorador provee a la funcion las caracteristica de poder funcionar como un endpoint
# es decir responder a una solicitud http del metodo GET al path /hello-world
@app.get("/hello-world")
def hello_world():
    # Automaticamente fastapi serializa los datos de python a json para transmitirlo al cliente que se comunico al endpoint
    return {"message": "Hello World"}


