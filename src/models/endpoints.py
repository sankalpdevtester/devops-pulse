```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EndpointBase(BaseModel):
    """Base endpoint model."""
    url: str
    method: str
    name: str

class EndpointCreate(EndpointBase):
    """Endpoint creation model."""
    org_id: int
    user_id: int

class EndpointUpdate(EndpointBase):
    """Endpoint update model."""
    id: Optional[int]

class Endpoint(EndpointBase):
    """Full endpoint model."""
    id: int
    org_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
```