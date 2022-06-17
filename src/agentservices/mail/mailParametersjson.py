
from pathlib import Path
import json
from src.domain.response.mailSendResponse import MailSendResponse

class MailParametersJson():
    
    def getDefaultEmailParameters() -> MailSendResponse:
        base_path = Path(__file__).parents[1]
        file_path = (base_path / "../config.json").resolve()
                    
        with open(file_path, 'r') as f:
            config = json.load(f)
    
        parametersRequired = {
            'end_point' : config['DefaulEmailSender']['END_POINT'],
            'canal' : config['DefaulEmailSender']['CANAL'],
            'id_transaccion' : config['DefaulEmailSender']['ID_TRANSACCION'],
            'user' : config['DefaulEmailSender']['USER'],
            'subject' : config['DefaulEmailSender']['SUBJECT'],
            'notification_sender' : config['DefaulEmailSender']['NOTIFICATION_SENDER'],
            'msj' : config['DefaulEmailSender']['MSJ'],
            'recipients' : config['DefaulEmailSender']['RECIPIENTS']
            #'proceso' = config['DefaulEmailSender']['PROCESO']
            #'nombre_proyecto' = config['DefaulEmailSender']['NOMBRE_PROYECTO']
        }
        
        parametersReq: MailSendResponse = MailSendResponse(**parametersRequired)   
        return parametersReq