from datetime import datetime
from pydantic import BaseModel

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