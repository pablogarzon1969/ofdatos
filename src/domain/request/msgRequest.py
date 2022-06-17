from enum import Enum

class MsgParametersRequest(Enum):
    
    #Parámetros WS
    msg = 'MSG'
    subject = 'SUBJECT'
    recipients = 'RECIPIENTS'