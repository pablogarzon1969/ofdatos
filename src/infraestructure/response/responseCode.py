from enum import Enum


class ResponseCode(Enum):
    TrasaccionExitosa = 200,
    TrasaccionExitosaSinDatos = 201
    PeticionIncorrecta = 400
    NoAutorizado = 401
    Prohibido = 403
    NoEncontrado = 404
