from pydantic import BaseModel


class LogData(BaseModel):
    message: str