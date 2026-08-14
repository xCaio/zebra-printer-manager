from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PrinterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    ip: str = Field(min_length=1, max_length=45)
    port: int = Field(default=9100, ge=1, le=65535)


class PrinterUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    ip: str | None = Field(default=None, min_length=1, max_length=45)
    port: int | None = Field(default=None, ge=1, le=65535)
    active: bool | None = None


class PrinterResponse(BaseModel):
    id: int
    name: str
    ip: str
    port: int
    active: bool
    created_at: datetime

class PrinterTestResponse(BaseModel):
    success: bool
    message: str
    printer: str


class PrinterStatusUpdate(BaseModel):
    active: bool

    model_config = ConfigDict(from_attributes=True)