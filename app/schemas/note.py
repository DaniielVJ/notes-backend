# Schema de las notas u estructura de cada nota
from datetime import datetime
from typing import Optional

# Nos permite definir el modelo de las entidades de la cual procesara los datos nuestra API
# definiendo un contrato de la estructura que debe tener.
from pydantic import BaseModel



# Aqui definimos la entidad de la cual procesaremos datos en el programa.
# y al mismo tiempo el esquema o estructura que estos deben tener.
class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime



# Creamos otro schema o modelo para Note pero para procesar los datos de la Nota que esperamos
# recibir del cliente de la API, los valores que no necesitamos que el cliente nos envie no lo agregamos
# ya que esos lo generamos nosotros
class CreateNote(BaseModel):
    title: str
    content: str
