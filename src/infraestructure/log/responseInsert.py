from  pydantic import BaseModel

class ResponseInsert(BaseModel):
    response: bool
