from typing import Dict, Any
from pydantic import BaseModel, Field, field_validator


class GameObject(BaseModel):
    id: str
    type: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    equipment: Dict[str, str] = Field(default_factory=dict)  # Now stores object IDs instead of objects

    @field_validator('id', 'type')
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("must not be empty")
        return v
