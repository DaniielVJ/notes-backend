# Schema de las notas u estructura de cada nota
from datetime import datetime
from typing import Optional

# Un schema de fastapi debe heredar de esta clase
from pydantic import BaseModel



# Aqui definimos la entidad de la cual procesaremos datos en el programa.
# y al mismo tiempo el esquema o estructura que estos deben tener.
class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


# Estos schemas son la estructura que deben seguir los datos que recibimos.


# Creamos otro schema o modelo para Note pero para procesar los datos de la Nota que esperamos
# recibir del cliente de la API, los valores que no necesitamos que el cliente nos envie no lo agregamos
# ya que esos lo generamos nosotros
class CreateNote(BaseModel):
    title: str
    content: str

    

# Schema que deben seguir los datos cuando se quiera actualizar una nota, un schema valido para la naturaleza de la actualizacion.
class UpdateNote(BaseModel):
    # Aqui definimos que si o si deben venir los datos en el json con un title y un content
    # pero pueden tener valor o no.


    # El tipo Optional es para indicar que no es obligatorio que se le asigne un valor
    title: Optional[str] = None
    content: Optional[str] = None


# SIEMPRE que vayamos a recibir datos en nuestra API, estos deben seguir el schema que creamos
# si no seran datos invalidos.