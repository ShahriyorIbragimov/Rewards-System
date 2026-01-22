from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    phone_number: str
    password: str

class TokenPayload(BaseModel):
    access_token: str
    token_type: str

class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None

class TelegramInitData(BaseModel):
    query_id: str
    user: TelegramUser
    auth_date: str
    signature: str
    hash: str

class InitDataPayload(BaseModel):
    init_data: str
