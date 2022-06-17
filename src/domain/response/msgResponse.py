from pydantic import BaseModel

class MsgParametersResponse (BaseModel):
    msg : str
    subject : str
    recipients : str