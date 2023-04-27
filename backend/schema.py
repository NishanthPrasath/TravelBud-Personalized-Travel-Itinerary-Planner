from pydantic import BaseModel
from typing import Union
from typing import List

class TokenClass(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserData(BaseModel):
    Username: str
    Password: str
    Name: str
    Plan: str
    AOI: List[str]