

#import win32com.client as win32
from enum import Enum
from src.infraestructure.log.loggingHandler import LoggingHandler
from datetime import datetime

class sendEmailRequest(Enum):
    mail_to = 'juan.aragon@axacolpatria.co'
    subject = 'Error during execution of project XXX'

class ErrorSendEmail():
    
    @classmethod
    def errorSendEmail(cls):
        try:
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = sendEmailRequest.mail_to.value
            mail.Subject = sendEmailRequest.subject.value
            msg = 'La ejecución del proyecto XXX realizada ' + str(datetime.now()) + ' falló. Este es el log de ejecución.'
            mail.Body = msg
            mail.HTMLBody = LoggingHandler.logIntoHtml()
        # 
        #To attach a file to the email (optional):
        #attachment  = "Path to the attachment"
        #mail.Attachments.Add(attachment)
            mail.Send()
            
        except Exception as ex:
            LoggingHandler.emit(0 ,'ERROR ENVIO CORREO', 'ENVIO CORREO', '', '', 'SI', str(ex))

