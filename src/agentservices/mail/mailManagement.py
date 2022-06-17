# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 16:55:21 2021

@author: ascastellanosc
"""
from datetime import datetime
from suds.client import Client
from suds.plugin import MessagePlugin
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.domain.response.mailSendResponse import MailSendResponse
import re

class EnvelopeFixer(MessagePlugin):
     def sending(self, context):
        context.envelope = re.sub(b'xmlns="http://AXAColpatria.Utilidad.Utilidad.Notificacion.Esquemas/EnviarCorreoEnLineaReq/V1.0"',b'',context.envelope)

class MailManagement():
    
    @classmethod
    def sudsToDict(cls, data):
        return dict([(str(key),val) for key, val in data])

    @classmethod
    def enviar_correo_ws(cls, mailParameters : MailSendResponse):
        
#        id_transaccion =  mailParameters.id_transaccion VALIDAR SI SE USA ESTO O NO
        
        try:
    
            time_stamp= str(datetime.now())
            time_stamp= time_stamp.replace(' ','T')
            time_stamp= time_stamp.split('.')[0]
            
            client = Client(mailParameters.end_point,plugins=[EnvelopeFixer()])

            enviarCorreoEnLineaReq = client.factory.create('ns1:EnviarCorreoEnLineaReq')
            
            enviarCorreoEnLineaReq.Header.IdCorrelacionConsumidor='1'
            enviarCorreoEnLineaReq.Header.Canal=mailParameters.canal
            enviarCorreoEnLineaReq.Header.PeticionFecha=time_stamp
            enviarCorreoEnLineaReq.Header.Usuario=mailParameters.user

            enviarCorreoEnLineaReq.Body.SendMailLineRequest.Subject=mailParameters.subject
            enviarCorreoEnLineaReq.Body.SendMailLineRequest.From= mailParameters.notification_sender

            Template = client.factory.create('ns1:Template')
            Template.Type='text/html'
            Template.Value=mailParameters.msj
            enviarCorreoEnLineaReq.Body.SendMailLineRequest.Template=Template
            
            recipients = mailParameters.recipients.split(',')

            for each in range(len(recipients)):
                recipientsL = client.factory.create('ns1:Recipients')
                recipientsL.To=[recipients[each]]
                enviarCorreoEnLineaReq.Body.SendMailLineRequest.Recipients.append(recipientsL)
                
            enviarCorreoEnLineaReq=cls.sudsToDict(enviarCorreoEnLineaReq)
            
            result = client.service.EnviarCorreoEnLinea(**enviarCorreoEnLineaReq)

            respuesta=str(result)

        
            if 'Status = "OK"' in respuesta and 'Description = "Delivery was created successfully"' in respuesta and 'RtaDescHost = "Procedimiento Realizado correctamente"' in respuesta:
                print("Se ha enviado la notificacion por correo electronico")
                LoggingHandler.emit(*LogCodification.email_sucess())
            else:
                print("Ha fallado el envio de la notificacion por correo electronico")
                
                
        except Exception as ex:
            ex = str(ex)
            print(ex)
            LoggingHandler.emit(*LogCodification.email_exception(ex))


 
                