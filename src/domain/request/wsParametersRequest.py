from enum import Enum

class wsParametersRequest(Enum):
    
    #Parámetros WS
    endPoint = 'END_POINT'
    canal = 'CANAL'
    idTransaction = 'ID_TRANSACCION'
    user = 'USER'
    msgSourceAbsent = 'MSG_FUENTE_AUSENTE'
    notifSender = 'NOTIF_SENDER'
    recipientsSourceAbsent = 'RECIPIENTS_FUENTE_AUSENTE'
    subjectSourceAbsent = 'SUBJECT_FUENTE_AUSENTE'
    msgProcessingSuccesful = 'MSG_PROCESAMIENTO_CORRECTO'
    msgProcessingIncorrect = 'MSG_PROCESAMIENTO_INCORRECTO'
    subjectProcessingSuccesful = 'SUBJECT_PROCESAMIENTO_CORRECTO'
    subjectProcessingIncorrect = 'SUBJECT_PROCESAMIENTO_INCORRECTO'
    recipientsProcessingSuccesful = 'RECIPIENTS_PROCESAMIENTO_CORRECTO'
    recipientsProcessingIncorrect = 'RECIPIENTS_PROCESAMIENTO_INCORRECTO'
    