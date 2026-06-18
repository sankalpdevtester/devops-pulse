from pydantic import BaseModel, validator
from typing import Optional

class Webhook(BaseModel):
    id: int
    url: str
    method: str

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith('http'):
            raise ValueError('URL must start with http')
        return v

    @validator('method')
    def validate_method(cls, v):
        if v not in ['POST', 'GET']:
            raise ValueError('Method must be POST or GET')
        return v

    class Config:
        orm_mode = True