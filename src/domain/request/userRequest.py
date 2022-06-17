from pydantic import BaseModel

class UserRequest(BaseModel):
    id: int
    username: str