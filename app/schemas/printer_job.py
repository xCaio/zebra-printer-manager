from datetime import datetime

from pydantic import BaseModel


class PrintJobCreate(BaseModel):
    printer_id: int
    layout_id: int
    quantity: int = 1
    data: dict


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