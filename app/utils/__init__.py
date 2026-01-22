from typing import Dict
def format_note_date_to_isoformat(note: Dict) -> Dict:
    # Pasamos la fecha y hora una cadena o string para poder transmitirla en el json
    note['created_at'] = note.get('created_at').isoformat()
    note['updated_at'] = note.get('updated_at').isoformat()
    return note