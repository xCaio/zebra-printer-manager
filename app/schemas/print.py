from datetime import datetime

from pydantic import BaseModel, Field


class PrintRequest(BaseModel):
    printer_id: int
    layout_id: int
    quantity: int = Field(default=1, ge=1)
    data: dict


class PrintResponse(BaseModel):
    success: bool
    message: str
    printer: str
    layout: str


class PrintJobResponse(BaseModel):
    id: int
    printer_id: int
    layout_id: int
    status: str
    quantity: int
    error_message: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class PrintJobListResponse(BaseModel):
    items: list[PrintJobResponse]
    total: int
    page: int
    limit: int
    pages: int