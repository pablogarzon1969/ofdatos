from enum import Enum

class LoggingDict(Enum):
    id_tarea = 'ID_TAREA'
    nom_tarea = 'NOM_TAREA'
    nom_proceso = 'NOM_PROCESO'
    object_py = 'OBJETO_PY'
    object_bd = 'OBJETO_BD'
    fail = 'FALLO'
    description = 'DESCRIPCION'