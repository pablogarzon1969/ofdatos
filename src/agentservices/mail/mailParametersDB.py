from ast import If
from src.data.repository.wsRepository import WsParametersRepository
from src.data.repository.wsRepository import WsParametersResponse
from src.domain.response.mailSendResponse import MailSendResponse
from src.data.repository.emailMsgRepository import MsgParametersRepository
from src.domain.response.msgResponse import MsgParametersResponse
from src.infraestructure.error.errorCategory import ErrorCategory
from src.infraestructure.log.loggingHandler import LoggingHandler

class MailParametersDb():
    @classmethod
    def getWSParameters(cls, process: str) -> MailSendResponse:
        responseRepository = None
        responseRepository = WsParametersRepository.getWsParameters(process)
        if responseRepository == None:
            return ErrorCategory.Business   
                
        if LoggingHandler.logCheckErrors() == 0: #Revisa si NO hay errores
            subject:str = responseRepository.subjectProcessingSuccesful
            msj:str = responseRepository.msgProcessingSuccesful
            recipients:str = responseRepository.recipientsProcessingSuccesful
        else:
            subject:str = responseRepository.subjectProcessingIncorrect
            msj:str = responseRepository.msgProcessingIncorrect
            recipients:str = responseRepository.recipientsProcessingIncorrect
        parametro_1:str = ''
        parametro_2:str = ''
        parametro_4:str = ''
        parametro_3:str = LoggingHandler.logIntoHtml()     
        
        parametersResponse: MailSendResponse = MailSendResponse(
            end_point = responseRepository.endPoint,
            canal = responseRepository.canal,
            id_transaccion = responseRepository.idTransaction,
            user = responseRepository.user,
            subject = subject,
            notification_sender = responseRepository.notifSender,
            msj = msj.format(parametro_1=parametro_1,parametro_2=parametro_2,parametro_3=parametro_3,parametro_4=parametro_4),
            recipients = recipients
        )   
        return parametersResponse

    @classmethod
    def getMsgParameters(cls, process: str) -> MailSendResponse:
        wsParameters : WsParametersResponse = WsParametersRepository.getWsParameters(process='WS')
        msgParameters : MsgParametersResponse = MsgParametersRepository.getMsgParameters(process)
        
        if isinstance(wsParameters, WsParametersResponse) and isinstance(msgParameters, MsgParametersResponse):
            logTable : str = LoggingHandler.logIntoHtml()
            parametersResponse: MailSendResponse = MailSendResponse(
                end_point = wsParameters.endPoint,
                canal = wsParameters.canal,
                id_transaccion = wsParameters.idTransaction,
                user = wsParameters.user,
                subject = msgParameters.subject,
                notification_sender = wsParameters.notifSender,
                msj = msgParameters.msg.format(logTable=logTable),
                recipients = msgParameters.recipients           
            )
        else:
            parametersResponse: MailSendResponse = None
            
        return parametersResponse
    