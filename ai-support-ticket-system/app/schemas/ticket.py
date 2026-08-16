from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: Optional[int]
    title: str
    description: str
    status: str
    priority: Optional[str]
    category: Optional[str]
    sentiment: Optional[str]
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime
