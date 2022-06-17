from typing import Any
from pydantic import BaseModel


class Log(BaseModel):
    message: str