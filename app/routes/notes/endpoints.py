# Modulo de todos los endpoints de notes

from typing import Dict, List

from fastapi import APIRouter, HTTPException
from google.cloud import firestore

from app.schemas import Note, CreateNote
from app.clients import get_firestore_client
from app.utils import format_note_date_to_isoformat

# Permite crear rutas o paths que podran consultar los clientes u definir los paths de los endpoints
router = APIRouter(prefix='/notes', tags=["notes"])


# Registramos en el router un endpoint que respondera al prefijo /notes y nada
@router.get("", status_code=200)
async def get_notes():
    client_firestore = get_firestore_client()
    collection = client_firestore.collection('notes').order_by('updated_at', direction=firestore.Query.DESCENDING)
    documents = collection.stream()
    notes = [format_note_date_to_isoformat(document.to_dict()) for document in documents]
    return {"notes": notes}



# Podemos definir en el decorador el status code que regresara el endpoint si sale todo exitosamente, en este
# caso regresaremos al cliente un 201, que significa que se creo el registro correctamente.
@router.post("", status_code=201)
async def create_note(note_data: CreateNote) -> Dict[str, Note]:
    # Los datos recibidos deben seguir la estructura o schema de un Create Note, poseer title y content de tipo str
    # Gracias a los schemas ya sabemos que esperamos recibir un title y un content desde el cliente.
    client_firestore = get_firestore_client()
    collection = client_firestore.collection("notes")

    # Creamos el documento vacio en la db de firestore
    doc_ref = collection.document()
    
    # Obtenemos la fecha y hora actual del servidor de firestore
    now = firestore.SERVER_TIMESTAMP

    # Creamos el diccionario con los datos de la nota que almacenaremos en el documento vacio de firestore
    new_note = {
        "id": doc_ref.id,
        "title": note_data.title,
        "content": note_data.content,
        "created_at": now,
        "updated_at": now
    }


    # Establecemos que el documento contendra como valor el diccionario con la nota
    doc_ref.set(new_note)

    # Obtenemos los datos tal cual como fueron almacenados en el documento de firestore
    doc = doc_ref.get()

    # Los datos del documento lo pasamos a un diccionario para poder manipularlos en el codigo python y 
    # formateamos los datetime a una cadena para poder transmitirlos en un json
    note = format_note_date_to_isoformat(doc.to_dict())
    
    # Retornamos un diccionario con la nota
    return {"note": note}


