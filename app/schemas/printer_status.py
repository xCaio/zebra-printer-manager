from pydantic import BaseModel


class PrinterStatusResponse(BaseModel):
    printer_id: int
    name: str
    ip: str
    port: int
    online: bool

class PrinterStatusListResponse(BaseModel):
    printers: list[PrinterStatusResponse]
    total: int