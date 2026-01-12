from pydantic import BaseModel

class UserLogin(BaseModel):
    phone_number: str
    password: str

class TokenPayload(BaseModel):
    access_token: str
    token_type: str
