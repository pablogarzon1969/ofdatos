from pydantic import BaseModel

class MailSendResponse(BaseModel):
    end_point: str
    canal: str
    id_transaccion: str
    user: str
    subject: str
    notification_sender: str
    msj: str
    recipients: str
