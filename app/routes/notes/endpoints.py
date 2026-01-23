# Modulo de todos los endpoints de notes

from typing import Dict, List

from fastapi import APIRouter, HTTPException
from google.cloud import firestore

from app.schemas import Note, CreateNote, UpdateNote
from app.clients import get_firestore_client
from app.utils import format_note_date_to_isoformat

# Un API Router es un objeto que permite crear multiples endpoints y sus paths que seran accesibles
# a partir del prefijo del APIRouter
router = APIRouter(prefix='/notes', tags=["notes"])


# Endpoint para obtener todas las notas
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




# Endpoint para obtener una unica nota por su id
@router.get("/{note_id}", status_code=200)
async def get_note_by_id(note_id: str) -> Dict[str, Note]:
    client_db = get_firestore_client()
    collection_ref = client_db.collection('notes')
    document_ref = collection_ref.document(note_id)
    document = document_ref.get()

    
    if not document.exists:
        # FastAPI captura este tipo de excepcion y la regresa como un response, donde recibira un json con el detail
        raise HTTPException(status_code=404, detail="Note not found")

    note = format_note_date_to_isoformat(document.to_dict())
    return {"note": note}
    


# Endpoint para actualizar parcialmente la nota, es decir no completa.
@router.patch('/{note_id}', status_code=200)
async def updated_note(note_id: str, note_data: UpdateNote) -> Dict[str, Note]: # Aqui definimos que los datos deben seguir el schema para ser validos
    client_db = get_firestore_client()
    collection_ref = client_db.collection('notes')
    # Vamos a buscar la nota a actualizar
    document_ref = collection_ref.document(note_id)
    # note_data: Se valida que los datos del json sigan ese schema y si lo siguen se crea una instancia UpdatedNote
    # a partir de los datos del json.
    doc = document_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Note not found")

    # Cramos un diccionario vacio que tendra los datos a actualizar y validamos si se enviaron datos
    updated_data = {}

    # Si recibimos el titulo lo agregamos al diccionario que actualizara los valores
    if note_data.title is not None:
        # Hacemos esto para aceptar string vacios como que quiere eliminar ese titulo o contenido y guardarla vacia
        updated_data['title'] = note_data.title
    
    # Si recibimos un contenido lo agregamos al diccionario que actualizara los valores
    if note_data.content is not None:
        updated_data['content'] = note_data.content


    # actualizamos tambien la fecha y hora de actualizacion
    updated_data['updated_at'] = firestore.SERVER_TIMESTAMP

    # .update(), solo actualiza los campos del documento que se encuentren en el diccionario
    document_ref.update(updated_data)

    # Obtenimos el documento al cual referencia el objeto, pero en este punto con los valores actualizados
    updated_doc = document_ref.get()

    # Formateamos el documento a un diccionario e isoformat y enviamos al usuario
    updated_note = format_note_date_to_isoformat(updated_doc.to_dict())

    return {"note": updated_note}



# Endpoint para eliminar una nota por el ID
@router.delete('/{note_id}', status_code=200)
async def delete_note(note_id: str) -> Dict[str, Note]:
    client_db = get_firestore_client()
    collection_ref = client_db.collection('notes')
    document_ref = collection_ref.document(note_id)
    # El metodo .get() nos regresa un snapshot de como se ve el documento en ese momento en la base de datos
    document = document_ref.get()


    # exists nos regresa si existia un documento con ese id para obtener un snapshot
    if not document.exists:
        raise HTTPException(status_code=404, detail="Note not found")

    document_ref.delete()

    # El snapshot que obtuvimos del documento en firestore antes de eliminar lo regresamos al usuario
    note = document.to_dict()

    return {"delete_note": format_note_date_to_isoformat(note)}




