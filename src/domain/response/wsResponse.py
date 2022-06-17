from pydantic import BaseModel

class WsParametersResponse (BaseModel):
    endPoint : str
    canal : str
    idTransaction : str
    user : str
    msgSourceAbsent : str
    notifSender : str
    recipientsSourceAbsent : str
    subjectSourceAbsent : str
    msgProcessingSuccesful : str
    msgProcessingIncorrect : str
    subjectProcessingSuccesful : str
    subjectProcessingIncorrect : str
    recipientsProcessingSuccesful : str
    recipientsProcessingIncorrect : str
    