from pydantic import BaseModel

class RegisterSchema(BaseModel):
    email: str
    full_name: str
    password: str
