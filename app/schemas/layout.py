from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class LayoutCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(
        default=None,
        max_length=200
    )
    zpl_template: str = Field(min_length=1)


class LayoutUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=200
    )

    zpl_template: str | None = Field(
        default=None,
        min_length=1
    )

    active: bool | None = None


class LayoutResponse(BaseModel):
    id: int
    name: str
    description: str | None
    zpl_template: str
    active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )